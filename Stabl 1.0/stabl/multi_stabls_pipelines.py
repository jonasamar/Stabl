import pandas as pd
import numpy as np
import os
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.feature_selection import VarianceThreshold
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LassoCV, LogisticRegressionCV, LogisticRegression, LinearRegression, ElasticNetCV,\
    Lasso
from sklearn.base import clone
from sklearn.model_selection import RepeatedStratifiedKFold, RepeatedKFold, LeaveOneOut
from sklearn.preprocessing import StandardScaler
from sklearn.svm import l1_min_c
from sklearn.metrics import roc_auc_score, average_precision_score, r2_score, mean_squared_error, mean_absolute_error


from multiprocessing import Process

from .metrics import jaccard_matrix
from .preprocessing import LowInfoFilter, remove_low_info_samples
from .stabl import save_stabl_results
from .visualization import boxplot_features, scatterplot_features, scatterplot_regression_predictions, boxplot_binary_predictions, plot_roc, plot_prc
from .utils import compute_CI, permutation_test_between_clfs

from scipy import stats
from scipy.stats import mannwhitneyu, spearmanr

from .pipelines_utils import save_plots # compute_scores_table

lasso = Lasso(max_iter=int(1e6))
lasso_cv = LassoCV(n_alphas=50, max_iter=int(1e6), n_jobs=-1)
en_cv = ElasticNetCV(n_alphas=50, max_iter=int(1e6), n_jobs=-1, l1_ratio=.5)

logit_lasso_cv = LogisticRegressionCV(penalty="l1", solver="liblinear", Cs=np.logspace(-2, 2, 50),
                                      max_iter=int(1e6), class_weight="balanced", scoring="roc_auc",
                                      n_jobs=-1
                                      )

logit_en_cv = LogisticRegressionCV(penalty="elasticnet", solver="saga", Cs=np.logspace(-2, 2, 50),
                                   max_iter=int(1e6), class_weight="balanced", scoring="roc_auc",
                                   n_jobs=-1, l1_ratios=[.5]
                                   )

logit = LogisticRegression(penalty=None, class_weight="balanced", max_iter=int(1e6))
linreg = LinearRegression()

preprocessing = Pipeline(
    steps=[
        ("variance", VarianceThreshold(0.01)),
        ("lif", LowInfoFilter()),
        ("impute", SimpleImputer(strategy="median")),
        ("std", StandardScaler())
    ]
)


def single_omic_multi_stabl_cv(
        X,
        y,
        outer_splitter,
        stablList,
        stabl_names,
        stability_selection,
        task_type,
        save_path,
        outer_groups=None
):
    """

    Parameters
    ----------
    X
    stability_selection: Stabl
    data_dict: dict
        Dictionary containing the input omic-files.

    y: pd.Series
        pandas Series containing the outcomes for the use case. Note that y should contains the union of outcomes for
        the data_dict.

    outer_splitter: sklearn.model_selection._split.BaseCrossValidator
        Outer cross validation splitter

    stablList: list of SurgeLibrary.stability_selection.StabilitySelection
        list of the STABL used to select features at each fold of the cross validation and for each omic.
        
    stabl_names: list of str
        list of the names of the STABL used to select features at each fold of the cross validation and for each omic.
        THEY HAVE TO BE IN THE SAME ORDER AS IN THE VARIABLE stabl

    task_type: str
        Can either be "binary" for binary classification or "regression" for regression tasks.

    save_path: Path or str
        Where to save the results

    outer_groups: pd.Series, default=None
        If used, should be the same size as y and should indicate the groups of the samples.

    Returns
    -------

    """
    models = ["SS 03", "SS 05", "SS 08", "Lasso", "Lasso 1SE", "ElasticNet"] + stabl_names # New pipeline : ["STABL"] was replaced by stabl_names

    os.makedirs(Path(save_path, "Training CV"), exist_ok=True)
    os.makedirs(Path(save_path, "Summary"), exist_ok=True)

    # Initializing the df containing the data of all omics
    predictions_dict = dict()
    selected_features_dict = dict()

    for model in models:
        predictions_dict[model] = pd.DataFrame(data=None, index=y.index)
        selected_features_dict[model] = []

    i = 1
    for train, test in outer_splitter.split(X, y, groups=outer_groups):
        # Jonas additional code in case outer_splitter is LeaveOneOut
        if isinstance(outer_splitter, LeaveOneOut):
            print(f" Iteration {i} over {X.shape[0]} ".center(80, '*'), "\n")
        elif isinstance(outer_groups, (list, tuple, np.ndarray, pd.Series, pd.DataFrame)):
            print(f" Iteration {i} over {outer_splitter.get_n_splits(groups=outer_groups)} ".center(80, '*'), "\n")
        else:
            print(f" Iteration {i} over {outer_splitter.get_n_splits()} ".center(80, '*'), "\n")
        # end additional code
        train_idx, test_idx = y.iloc[train].index, y.iloc[test].index

        fold_selected_features = dict()
        for model in models:
            fold_selected_features[model] = []

        print(f"{len(train_idx)} train samples, {len(test_idx)} test samples")

        X_tmp = X.drop(index=test_idx, errors="ignore")

        # Preprocessing of X_tmp
        X_tmp = remove_low_info_samples(X_tmp)
        y_tmp = y.loc[X_tmp.index]

        X_tmp_std = pd.DataFrame(
            data=preprocessing.fit_transform(X_tmp),
            index=X_tmp.index,
            columns=preprocessing["std"].get_feature_names_out()
        )

        # __STABL__
        if task_type == "binary":
            min_C = l1_min_c(X_tmp_std, y_tmp)
            lambda_grid = np.linspace(min_C, min_C * 100, 10)
            stability_selection.set_params(lambda_grid=lambda_grid)
            for id, stabl_model in enumerate(stablList): # New pipeline : a loop is required to go through the different STABL models
                stabl_model.set_params(lambda_grid=lambda_grid)
                stabl_model.fit(X_tmp_std, y_tmp)
                tmp_sel_features = list(stabl_model.get_feature_names_out())
                fold_selected_features[stabl_names[id]] = tmp_sel_features
                print(
                    f"{stabl_names[id]} finished ({X_tmp.shape[0]} samples);"
                    f" {len(tmp_sel_features)} features selected\n"
                )

        # __SS__
        stability_selection.fit(X_tmp_std, y_tmp)
        fold_selected_features["SS 03"] = list(stability_selection.get_feature_names_out(new_hard_threshold=.3))
        fold_selected_features["SS 05"] = list(stability_selection.get_feature_names_out(new_hard_threshold=.5))
        fold_selected_features["SS 08"] = list(stability_selection.get_feature_names_out(new_hard_threshold=.8))

        for id, stabl_model in enumerate(stablList): 
            selected_features_dict[stabl_names[id]].append(fold_selected_features[stabl_names[id]])
        selected_features_dict[f"SS 03"].append(fold_selected_features["SS 03"])
        selected_features_dict[f"SS 05"].append(fold_selected_features["SS 05"])
        selected_features_dict[f"SS 08"].append(fold_selected_features["SS 08"])

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for id, stabl_model in enumerate(stablList): 
            print(f"This fold: {len(fold_selected_features[stabl_names[id]])} features selected for {stabl_names[id]}")
        print(f"This fold: {len(fold_selected_features['SS 03'])} features selected for SS 03")
        print(f"This fold: {len(fold_selected_features['SS 05'])} features selected for SS 05")
        print(f"This fold: {len(fold_selected_features['SS 08'])} features selected for SS 08")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        for model in stabl_names + ["SS 03", "SS 05", "SS 08"]: # New pipeline : ["STABL"] was replaced by stabl_names

            X_train = X.loc[train_idx, fold_selected_features[model]]
            X_test = X.loc[test_idx, fold_selected_features[model]]
            y_train, y_test = y.loc[train_idx], y.loc[test_idx]

            if len(fold_selected_features[model]) > 0:
                # Standardization
                std_pipe = Pipeline(
                    steps=[
                        ('imputer', SimpleImputer(strategy="median")),
                        ('std', StandardScaler())
                    ]
                )

                X_train = pd.DataFrame(
                    data=std_pipe.fit_transform(X_train),
                    index=X_train.index,
                    columns=X_train.columns
                )
                X_test = pd.DataFrame(
                    data=std_pipe.transform(X_test),
                    index=X_test.index,
                    columns=X_test.columns
                )

                # __Final Models__
                if task_type == "binary":
                    predictions = clone(logit).fit(X_train, y_train).predict_proba(X_test)[:, 1].flatten()

                elif task_type == "regression":
                    predictions = clone(linreg).fit(X_train, y_train).predict(X_test)

                else:
                    raise ValueError("task_type not recognized.")

                predictions_dict[model].loc[test_idx, f'Fold n°{i}'] = predictions

            else:
                if task_type == "binary":
                    predictions_dict[model].loc[test_idx, f'Fold n°{i}'] = [0.5] * len(test_idx)

                elif task_type == "regression":
                    predictions_dict[model].loc[test_idx, f'Fold n°{i}'] = [np.mean(y_train)] * len(test_idx)

                else:
                    raise ValueError("task_type not recognized.")

        # __other models__
        X_train = X.loc[train_idx]
        X_test = X.loc[test_idx]
        X_train = pd.DataFrame(
            data=preprocessing.fit_transform(X_train),
            columns=preprocessing["std"].get_feature_names_out(),
            index=X_train.index
        )

        X_test = pd.DataFrame(
            data=preprocessing.transform(X_test),
            columns=preprocessing["std"].get_feature_names_out(),
            index=X_test.index
        )

        # __Lasso__
        if task_type == "binary":
            inner_splitter = RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=42)
            model = clone(logit_lasso_cv).set_params(cv=inner_splitter)
            predictions = model.fit(X_train, y_train).predict_proba(X_test)[:, 1]
        else:
            inner_splitter = RepeatedKFold(n_splits=5, n_repeats=5, random_state=42)
            model = clone(lasso_cv).set_params(cv=inner_splitter)
            predictions = model.fit(X_train, y_train).predict(X_test)

        selected_features_dict["Lasso"].append(list(X_train.columns[np.where(model.coef_.flatten())]))
        predictions_dict["Lasso"].loc[test_idx, f"Fold n°{i}"] = predictions

        # __Lasso 1SE__
        if task_type == "binary":
            new_best_c_corr = model.C_[0] - model.scores_[True].std() / np.sqrt(inner_splitter.get_n_splits())
            if new_best_c_corr < 0:
                best_c_corr = abs(model.C_[0])
            else:
                best_c_corr = new_best_c_corr
            model = LogisticRegression(penalty='l1', solver='liblinear', C=best_c_corr, class_weight='balanced',
                                       max_iter=2_000_000)
            predictions = model.fit(X_train, y_train).predict_proba(X_test)[:, 1]

        selected_features_dict["Lasso 1SE"].append(list(X_train.columns[np.where(model.coef_.flatten())]))
        predictions_dict["Lasso 1SE"].loc[test_idx, f"Fold n°{i}"] = predictions

        # __EN__
        if task_type == "binary":
            model = clone(logit_en_cv).set_params(cv=inner_splitter)
            predictions = model.fit(X_train, y_train).predict_proba(X_test)[:, 1]

        else:
            model = clone(en_cv).set_params(cv=inner_splitter)
            predictions = model.fit(X_train, y_train).predict(X_test)

        selected_features_dict["ElasticNet"].append(list(X_train.columns[np.where(model.coef_.flatten())]))
        predictions_dict["ElasticNet"].loc[test_idx, f"Fold n°{i}"] = predictions

        i += 1

    # __SAVING_RESULTS__

    if y.name is None:
        y.name = "outcome"

    summary_res_path = Path(save_path, "Summary")
    cv_res_path = Path(save_path, "Training CV")

    jaccard_matrix_dict = dict()
    formatted_features_dict = dict()

    for model in models:

        jaccard_matrix_dict[model] = jaccard_matrix(selected_features_dict[model])
        
        # Jonas additional code in case outer_splitter is LeaveOneOut
        if isinstance(outer_splitter, LeaveOneOut):
            index=[f"Fold {i}" for i in range(X.shape[0])]
        elif isinstance(outer_groups, (list, tuple, np.ndarray, pd.Series, pd.DataFrame)):
            index=[f"Fold {i}" for i in range(outer_splitter.get_n_splits(groups=outer_groups))]
        else:
            index=[f"Fold {i}" for i in range(outer_splitter.get_n_splits())]
        # end additional code

        formatted_features_dict[model] = pd.DataFrame(
            data={
                "Fold selected features": selected_features_dict[model],
                "Fold nb of features": [len(el) for el in selected_features_dict[model]]
            },
            index=index # Jonas'additional code linked to this parameter
        )
        formatted_features_dict[model].to_csv(Path(cv_res_path, f"Selected Features {model}.csv"))

    predictions_dict = {model: predictions_dict[model].median(axis=1) for model in predictions_dict.keys()}

    table_of_scores = new_compute_scores_table( # New pipeline : calling new_compute_scores_table instead of compute_scores_table
        stabl_names,
        predictions_dict=predictions_dict,
        y=y,
        task_type=task_type,
        selected_features_dict=formatted_features_dict
    )

    table_of_scores.to_csv(Path(summary_res_path, "Scores training CV.csv"))
    table_of_scores.to_csv(Path(cv_res_path, "Scores training CV.csv"))

    save_plots(
        predictions_dict=predictions_dict,
        y=y,
        task_type=task_type,
        save_path=cv_res_path
    )
    
    # New pipeline : Univariate Analysis
    resultFolderUnivariate = save_path+"/Univariate/"
    
    if task_type == 'binary':
        os.makedirs(resultFolderUnivariate, exist_ok=True)
        
        vals1 = []
        vals2 = []
        for col in X.columns:
            a,b = mannwhitneyu(X.loc[y == 0,col].to_numpy(),X.loc[y == 1,col].to_numpy())
            vals1.append(a)
            vals2.append(b)
            
        res = pd.DataFrame(data=[vals1,vals2],index= ["Mann-Whitney U-test","p-value"],columns=X.columns)
        res = res.sort_values(by="p-value",axis=1)
        res.T.to_csv(Path(resultFolderUnivariate + "Mann-WhitneyU-testPval.csv"))
            

        boxplot_features(
            list_of_features=res.columns[:10],
            df_X=X[res.columns[:10]],
            y=y,
            show_fig=False,
            export_file=True,
            path = Path(resultFolderUnivariate)
            )
        
    elif task_type == 'regression':
        os.makedirs(resultFolderUnivariate, exist_ok=True)
        
        Spearmancorr = {}

        features = X.columns

        for feature in features:
            corr, pval = spearmanr(X[feature], y)
            Spearmancorr[feature] = [corr, pval]

        SpearmanPvalue = pd.DataFrame(Spearmancorr).T
        SpearmanPvalue.columns = ['Spearman corr', 'pvalue']
        SpearmanPvalue.sort_values('pvalue', inplace=True)
        SpearmanPvalue.to_csv(Path(resultFolderUnivariate + 'SpearmanCorrelationsPval.csv'), index=True)
        
        scatterplot_features(
            SpearmanPvalue[:10].index,
            X,
            y,
            show_fig=False,
            export_file=True,
            path=Path(resultFolderUnivariate))
        
    # New pipeline : Final STABLs
        
    preprocessing2 = Pipeline(
        steps=[
        ("lif", LowInfoFilter(0.2)),
        ("variance", VarianceThreshold(0.01)),
        ("impute", SimpleImputer(strategy="median")),
        ("std", StandardScaler())
        ]
    )

    dataSTD = pd.DataFrame(
        data=preprocessing2.fit_transform(X),
        index=X.index,
        columns=preprocessing2.get_feature_names_out()
    )
        
    for id, stabl_model in enumerate(stablList):
        stabl = clone(stabl_model)
        stabl.fit(dataSTD,y.astype(int))

        resultFolder = save_path 
        save_stabl_results(stabl_model,resultFolder+"/FinalSTABLs/"+ stabl_names[id],dataSTD,y,task_type=task_type)

    return predictions_dict

def new_compute_scores_table(
        stabl_names,
        predictions_dict,
        y,
        task_type="binary",
        selected_features_dict=None
):
    """Function to output the table of scores
    for a STABL against Lasso benchmark on a single omic.

    Parameters
    ----------
    selected_features_dict
    predictions_dict: dict
        Dictionary of raw predictions (should contain a "Lasso" key).

    y: pd.Series
        pandas Series containing the outcomes.

    task_type: string, default="binary"
        Type of task, can either be "binary" or "regression".

    Returns
    -------
    table_of_scores: pd.DataFrame
    """

    scores_columns = []
    if selected_features_dict is not None:
        if task_type == "binary":
            scores_columns = ["ROC AUC", "Average Precision", "N features", "CVS"]

        elif task_type == "regression":
            scores_columns = ["R2", "RMSE", "MAE", "N features", "CVS"]
            
    else:
        if task_type == "binary":
            scores_columns = ["ROC AUC", "Average Precision"]

        elif task_type == "regression":
            scores_columns = ["R2", "RMSE", "MAE"]

    table_of_scores = pd.DataFrame(data=None, columns=scores_columns)

    for model, preds in predictions_dict.items():
        stabl_preds = predictions_dict[stabl_names[0]] # New pipeline
        # Jonas : I chose by default the first STABL model of the list as reference for the permutation tests
        
        if task_type == "binary":
            model_roc = roc_auc_score(y, preds)
            model_roc_CI = compute_CI(y, preds, scoring="roc_auc")
            cell_value = f"{model_roc:.3f} [{model_roc_CI[0]:.3f}, {model_roc_CI[1]:.3f}]"
            if model != stabl_names[0]:
                p_value = permutation_test_between_clfs(y, preds, stabl_preds, scoring="roc_auc")[1]
                cell_value = cell_value + f" (p={p_value})"
            table_of_scores.loc[model, "ROC AUC"] = cell_value

            model_ap = average_precision_score(y, preds)
            model_ap_CI = compute_CI(y, preds, scoring="average_precision")
            cell_value = f"{model_ap:.3f} [{model_ap_CI[0]:.3f}, {model_ap_CI[1]:.3f}]"
            if model != stabl_names[0]:
                p_value = permutation_test_between_clfs(y, preds, stabl_preds, scoring="average_precision")[1]
                cell_value = cell_value + f" (p={p_value})"
            table_of_scores.loc[model, "Average Precision"] = cell_value

        elif task_type == "regression":
            model_r2 = r2_score(y, preds)
            model_r2_CI = compute_CI(y, preds, scoring="r2")
            table_of_scores.loc[model, "R2"] = f"{model_r2:.3f} [{model_r2_CI[0]:.3f}, {model_r2_CI[1]:.3f}]"

            model_rmse = np.sqrt(mean_squared_error(y, preds))
            model_rmse_CI = compute_CI(y, preds, scoring="rmse")
            table_of_scores.loc[model, "RMSE"] = f"{model_rmse:.3f} [{model_rmse_CI[0]:.3f}, {model_rmse_CI[1]:.3f}]"

            model_mae = mean_absolute_error(y, preds)
            model_mae_CI = compute_CI(y, preds, scoring="mae")
            table_of_scores.loc[model, "MAE"] = f"{model_mae:.3f} [{model_mae_CI[0]:.3f}, {model_mae_CI[1]:.3f}]"

        if selected_features_dict is not None:
            for stabl in stabl_names: # New pipeline : required to loop over the several STABL models (there used to be only one)
                sel_features_stabl = selected_features_dict[stabl]["Fold nb of features"]
                jaccard_mat_stabl = jaccard_matrix(selected_features_dict[stabl]["Fold selected features"], remove_diag=False)
                jaccard_val_stabl = jaccard_mat_stabl[np.triu_indices_from(jaccard_mat_stabl, k=1)]
    
                median_features = np.median(sel_features_stabl)
                iqr_features = np.quantile(sel_features_stabl, [.25, .75])
                cell_value = f"{median_features:.3f} [{iqr_features[0]:.3f}, {iqr_features[1]:.3f}]"
                table_of_scores.loc[stabl, "N features"] = cell_value
    
                jaccard_median = np.median(jaccard_val_stabl)
                jaccard_iqr = np.quantile(jaccard_val_stabl, [.25, .75])
                cell_value = f"{jaccard_median:.3f} [{jaccard_iqr[0]:.3f}, {jaccard_iqr[1]:.3f}]"
                table_of_scores.loc[stabl, "CVS"] = cell_value

            if not model in stabl_names: # New pipeline : used to be "if model != 'STABL':"
                sel_features = selected_features_dict[model]["Fold nb of features"]
                jaccard_mat = jaccard_matrix(selected_features_dict[model]["Fold selected features"], remove_diag=False)
                jaccard_val = jaccard_mat[np.triu_indices_from(jaccard_mat, k=1)]
                p_value_feature = mannwhitneyu(x=sel_features, y=sel_features_stabl).pvalue
                p_value_feature = f" (p={p_value_feature:.3e})"
                p_value_cvs = mannwhitneyu(x=jaccard_val, y=jaccard_val_stabl).pvalue
                p_value_cvs = f" (p={p_value_cvs:.3e})"

                median_features = np.median(sel_features)
                iqr_features = np.quantile(sel_features, [.25, .75])
                cell_value = f"{median_features:.3f} [{iqr_features[0]:.3f}, {iqr_features[1]:.3f}]" + p_value_feature
                table_of_scores.loc[model, "N features"] = cell_value

                jaccard_median = np.median(jaccard_val)
                jaccard_iqr = np.quantile(jaccard_val, [.25, .75])
                cell_value = f"{jaccard_median:.3f} [{jaccard_iqr[0]:.3f}, {jaccard_iqr[1]:.3f}]" + p_value_cvs
                table_of_scores.loc[model, "CVS"] = cell_value

    return table_of_scores
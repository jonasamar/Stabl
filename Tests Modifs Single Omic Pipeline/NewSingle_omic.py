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

from stabl.metrics import jaccard_matrix
from stabl.preprocessing import LowInfoFilter, remove_low_info_samples
from stabl.stabl import save_stabl_results
from stabl.visualization import boxplot_features

from scipy import stats
from scipy.stats import mannwhitneyu

from stabl.pipelines_utils import save_plots, compute_scores_table

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


def new_single_omic_stabl_cv(
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
    models = ["SS 03", "SS 05", "SS 08", "Lasso", "Lasso 1SE", "ElasticNet"] + stabl_names

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
            columns=preprocessing.get_feature_names_out()
        )

        # __STABL__
        if task_type == "binary":
            min_C = l1_min_c(X_tmp_std, y_tmp)
            lambda_grid = np.linspace(min_C, min_C * 100, 10)
            stability_selection.set_params(lambda_grid=lambda_grid)
            for id, stabl_model in enumerate(stablList):
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

        selected_features_dict["STABL"].append(fold_selected_features["STABL"])
        selected_features_dict[f"SS 03"].append(fold_selected_features["SS 03"])
        selected_features_dict[f"SS 05"].append(fold_selected_features["SS 05"])
        selected_features_dict[f"SS 08"].append(fold_selected_features["SS 08"])

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(f"This fold: {len(fold_selected_features['STABL'])} features selected for STABL")
        print(f"This fold: {len(fold_selected_features['SS 03'])} features selected for SS 03")
        print(f"This fold: {len(fold_selected_features['SS 05'])} features selected for SS 05")
        print(f"This fold: {len(fold_selected_features['SS 08'])} features selected for SS 08")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        for model in stabl_names + ["SS 03", "SS 05", "SS 08"]:

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
            columns=preprocessing.get_feature_names_out(),
            index=X_train.index
        )

        X_test = pd.DataFrame(
            data=preprocessing.transform(X_test),
            columns=preprocessing.get_feature_names_out(),
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

    table_of_scores = compute_scores_table(
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
    
    # Univariate Analysis
    
    if task_type == 'binary':
        resultFolderUnivariate = save_path+"/Univariate/"
        
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
    
        # Final STABL
        
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

            resultFolder = save_path + stabl_names[id]
            save_stabl_results(stabl_model,resultFolder+"/FinalSTABL/"+stabl_names[id],dataSTD,y,task_type="binary")

    return predictions_dict
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold
from stabl.preprocessing import LowInfoFilter
from stabl.stabl import Stabl, save_stabl_results
from sklearn.base import clone
from sklearn.linear_model import Lasso,ElasticNet,LogisticRegression
from sklearn.model_selection import LeaveOneOut
from scipy.stats import mannwhitneyu
from stabl.visualization import scatterplot_features,boxplot_features
from stabl.single_omic_pipelines import single_omic_stabl, single_omic_stabl_cv
from pathlib import Path
import argparse
import os

# lasso = Lasso(max_iter=int(1e6))
# en05_05 = ElasticNet(max_iter=int(1e6))

# stabl_regression = Stabl(
#     base_estimator=clone(lasso),
#     lambda_grid=np.logspace(0.01, 2, 30),
#     lambda_name="alpha",
#     artificial_type="knockoff",
#     artificial_proportion=1,
#     n_bootstraps=1000,
#     random_state=42
# )

logit_lasso = LogisticRegression(penalty="l1", max_iter=int(1e6), solver="liblinear", class_weight="balanced")
logit_en05 = LogisticRegression(penalty="elasticnet", l1_ratio = 0.5, max_iter=int(1e6), solver="saga", class_weight="balanced")

stabl_class = Stabl(
    base_estimator=clone(logit_lasso),
    lambda_name="C",
    lambda_grid=np.linspace(0.01, 1, 30),
    artificial_type="knockoff",
    fdr_threshold_range=np.arange(0.1, 1, 0.01),
    n_bootstraps=1000,
    random_state=42
)

stablList = [clone(stabl_class),clone(stabl_class).set_params(artificial_type="random_permutation"),
             clone(stabl_class).set_params(base_estimator=clone(logit_en05)),
             clone(stabl_class).set_params(base_estimator=clone(logit_en05),artificial_type="random_permutation")]
stablNames = ["L-KF","L-RP","EN05-KF","EN05-RP"]

#outer_splitter = LeaveOneOut()
outer_splitter = RepeatedStratifiedKFold(n_splits=5, n_repeats=4, random_state=42)

stability_selection = clone(stabl_class).set_params(artificial_type=None, hard_threshold=0.3)


def run():
    X_train = pd.read_csv('../Sample Data/COVID-19/Training/Proteomics.csv',index_col="sampleID")
    X_val = pd.read_csv("../Sample Data/COVID-19/Validation/Validation_proteomics.csv", index_col=0)
    y_val = pd.read_csv("../Sample Data/COVID-19/Validation/Validation_outcome(WHO.0 ≥ 5).csv", index_col=0).iloc[:,0]
    y_train = pd.read_csv("../Sample Data/COVID-19/Training/Mild&ModVsSevere.csv", index_col=0).iloc[:, 0]
        
    data = pd.concat([X_train, X_val])
    label = pd.concat([y_train, y_val])

    new_single_omic_stabl_cv(
    X=X_train,
    y=y_train.astype(int),
    outer_splitter=outer_splitter,
    stablList=stablList,
    stabl_names=stablNames,
    stability_selection=stability_selection,
    task_type="binary",
    save_path='./Results',
    )
    
run()

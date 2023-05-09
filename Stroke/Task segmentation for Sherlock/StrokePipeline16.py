import warnings
warnings.filterwarnings('ignore')
# Libraries
## Basic libraries
import numpy as np
import pandas as pd
from pathlib import Path
import os
import csv

from sklearn.model_selection import LeaveOneOut, RepeatedStratifiedKFold, RepeatedKFold
from sklearn.base import clone

from stabl.stabl import Stabl, plot_stabl_path, plot_fdr_graph, save_stabl_results
from stabl.preprocessing import LowInfoFilter, remove_low_info_samples

## Stabl pipelines
from stabl.single_omic_pipelines import single_omic_stabl, single_omic_stabl_cv
from stabl.pipelines_utils import compute_features_table, save_plots
from stabl.stacked_generalization import stacked_multi_omic
from stabl.visualization import plot_prc, plot_roc

# Data
## Importing dataset
dataset = pd.read_csv("./Sample Data/Stroke/preprocessed_HT.csv")
dataset['population'] = dataset['population'].apply(lambda x : x.replace('*', ''))
dataset['group'][dataset['group']=='No']=0
dataset['group'][dataset['group']=='Yes']=1

def stroke_pipeline(time, cellpop):
    """Function to execute the stabl pipeline on the preprocessed_HT.csv file
    on a specific kind of cell population and at a given time (cf description of
    dataset above for more explanations).
    It will create files and folders with the data on which the stabl pipeline is run
    and oreder the results similarly as Benchmarks notebooks in the Notebook example folder.
    It will additionally provide a univariate analysis of the features in the Univariate folder.

    Parameters
    ----------
    time : str
        'P1' : day of surgery
        'P2' : day after surgery
        'P3' : 30 days after surgery
        'Delta' : P2 - P1
        
    cellpop : str
        element of ['Bcells', 'CCR2nncMC', 'CCR2pcMC', 'CD41hiCD61hiPLT', 'CD4Tcm',
                    'CD4Tem', 'CD4Tnaive', 'CD4Trm', 'CD56brightCD16nNKcells',
                    'CD56dimCD16pNKcells', 'CD61pCD41pPLT', 'CD62LnAgedNeutrophils',
                    'CD62LpImmatureNeutrophils', 'CD8Tcm', 'CD8Tem', 'CD8Tnaive',
                    'CD8Trm', 'gdTcells', 'intMC', 'mDC', 'MDSC', 'NKT', 'pDC',
                    'Th1mem', 'Th1naive', 'Tregmem', 'Tregnaive']
        indicating the type of cells we are looking at

    Returns
    -------
    models_prediction : dictionary of dataframes
        dictionary containing the predictions of each model.

    """
    
    if not time in ['P1', 'P2', 'P3', 'Delta']:
        print(time + ' is not recognized : chose between "P1", "P2", "P3"')
        return

    if not cellpop in ['Bcells', 'CCR2nncMC', 'CCR2pcMC', 'CD41hiCD61hiPLT', 'CD4Tcm',
                        'CD4Tem', 'CD4Tnaive', 'CD4Trm', 'CD56brightCD16nNKcells',
                        'CD56dimCD16pNKcells', 'CD61pCD41pPLT', 'CD62LnAgedNeutrophils',
                        'CD62LpImmatureNeutrophils', 'CD8Tcm', 'CD8Tem', 'CD8Tnaive',
                        'CD8Trm', 'gdTcells', 'intMC', 'mDC', 'MDSC', 'NKT', 'pDC',
                        'Th1mem', 'Th1naive', 'Tregmem', 'Tregnaive']:
        print(cellpop + 'not recognized, look description of the dataset above and chose a valid cell population.')

    # Save Paths
    data_path = Path('./Stroke', 'Data', time, cellpop)
    os.makedirs(data_path, exist_ok=True)
    os.makedirs('./Stroke/Results', exist_ok=True)
    
    # Data
    if time == 'Delta':
        data1 = dataset[(dataset['population']==cellpop) & (dataset['time']=='P1')]
        data2 = dataset[(dataset['population']==cellpop) & (dataset['time']=='P2')]

        # Rearrangement of the dataset
        dict_x1 = {}
        dict_x2 = {}
        dict_y = {}
        for sample in data1['sampleID']:
            dict_x1[sample] = {}
            dict_x2[sample] = {}
            for feature in data1['reagent'].unique():
                mask1 = (data1['sampleID']==sample) & (data1['reagent']==feature)
                mask2 = (data2['sampleID']==sample) & (data2['reagent']==feature)
                dict_x1[sample][feature] = float(data1[mask1]['feature'])
                dict_x2[sample][feature] = float(data2[mask2]['feature'])
            dict_y[sample] = data1[data1['sampleID']==sample]['group'].iloc[0]

        X1 = pd.DataFrame(dict_x1).T
        X2 = pd.DataFrame(dict_x2).T
        X = X2 - X1
        X.to_csv(Path(data_path, "X.csv"), index=True)
    else : 
        data = dataset[(dataset['population']==cellpop) & (dataset['time']==time)]
    
        # Rearrangement of the dataset
        dict_x = {}
        dict_y = {}
        for sample in data['sampleID']:
            dict_x[sample] = {}
            for feature in data['reagent'].unique():
                mask = (data['sampleID']==sample) & (data['reagent']==feature)
                dict_x[sample][feature] = float(data[mask]['feature'])
            dict_y[sample] = data[data['sampleID']==sample]['group'].iloc[0]
            
        pd.DataFrame(dict_x).T.to_csv(Path(data_path, "X.csv"), index=True)
    pd.DataFrame([dict_y]).T.to_csv(Path(data_path, "y.csv"), index=True)
    
    X = pd.read_csv(Path(data_path, "X.csv"), index_col=0)
    y = pd.read_csv(Path(data_path, "y.csv"), index_col=0).iloc[:, 0]
    y.name = None
    
    # Multivariate Analysis
    
    result_folder = "./Stroke/Results/" + time + "/" + cellpop + "_Results" 
    
    import numpy as np
    
    ### Single-omic Training-CV
    stabl = Stabl(
        lambda_grid=np.linspace(0.01, 5, 10),
        n_bootstraps=1000,
        artificial_type="random_permutation",
        replace=False,
        fdr_threshold_range=np.arange(0.1, 1, 0.01),
        sample_fraction=.5,
        random_state=42
    )

    stability_selection = clone(stabl).set_params(hard_threshold=.1, artificial_type = None)
    outer_splitter = RepeatedKFold(n_splits=len(X), n_repeats=10, random_state=42)
    
    from stabl.single_omic_pipelines import single_omic_stabl_cv, single_omic_stabl

    predictions_dict = single_omic_stabl_cv(
        X=X,
        y=y,
        outer_splitter=outer_splitter,
        stabl=stabl,
        stability_selection=stability_selection,
        task_type="binary",
        save_path=result_folder,
        outer_groups=None
    )
    
    np.random.seed(1)
    stabl_singl = Stabl(
        lambda_grid=np.linspace(0.01, 5, 10),
        n_bootstraps=1000,
        artificial_proportion=1.,
        artificial_type="random_permutation",
        hard_threshold=None,
        replace=False,
        fdr_threshold_range=np.arange(0.1, 1, 0.01),
        sample_fraction=.5,
        random_state=42
    )

    stability_selection = clone(stabl_singl).set_params(artificial_type=None, hard_threshold=.1)
    predictions_dict = single_omic_stabl(
        X=X,
        y=y,
        stabl=stabl_singl,
        stability_selection=stability_selection,
        task_type="binary",
        save_path=Path(result_folder),
    )
    
    ### Tables of features
    selected_features_dict = dict()
    for model in ["STABL", "Lasso", "Lasso 1SE", "ElasticNet", "SS 03", "SS 05", "SS 08"]:
        path = Path(result_folder, "Training-Validation", f"{model} coefficients.csv")
        try:
            selected_features_dict[model] = list(pd.read_csv(path, index_col=0).iloc[:, 0].index)
        except:
            selected_features_dict[model] = []
            
    features_table = compute_features_table(
        selected_features_dict,
        X_train=X,
        y_train=y,
        X_test=None,
        y_test=None,
        task_type="binary")

    features_table.to_csv(Path(result_folder, "Training-Validation", "Table of features.csv"))
    
    # Univariate
    from scipy.stats import spearmanr

    Spearmancorr = {}

    features = X.columns

    for feature in features:
        
        corr, pval = spearmanr(X[feature], y)
        Spearmancorr[feature] = [corr, pval]

    SpearmanPvalue = pd.DataFrame(Spearmancorr).T
    SpearmanPvalue.columns = ['Spearman corr', 'pvalue']
    SpearmanPvalue.sort_values('pvalue', inplace=True)
    SpearmanPvalue.to_csv(Path(result_folder, 'Summary', 'SpearmanCorrelationsPval.csv'), index=True)
    
    from stabl.visualization import boxplot_features

    os.makedirs(Path(result_folder, 'Univariate'), exist_ok=True)

    boxplot_features(
            SpearmanPvalue[:10].index,
            X,
            y,
            show_fig=False,
            export_file=True,
            path=Path(result_folder, 'Univariate'))
    
    # Rearrangement of the results
    import shutil

    ## Copying the boxplots in the summary folder
    for model in ["STABL", "Lasso", "Lasso 1SE", "ElasticNet", "SS 03", "SS 05", "SS 08"]:
        src_folder = Path(result_folder, 'Training CV', model)
        dst_folder = Path(result_folder, 'Summary')
        for filename in os.listdir(src_folder):
            if "Boxplot" in filename:
                src_file = os.path.join(src_folder, filename)
                dst_file = os.path.join(dst_folder, filename)
                shutil.copy(src_file, dst_file)
    
    ## Adding the pvalue and Pearson Correlation to the scores training CV.csv file
    from PyPDF2 import PdfReader
    import csv

    def get_pvalue_from_Boxplot(model):
        reader = PdfReader(Path(result_folder, 'Summary', model + ' Boxplot of median predictions.pdf'))         
        # getting a specific page from the pdf file
        page = reader.pages[0]
        # extracting text from page
        text = page.extract_text()
        start_index = text.find('U-test pvalue = ') + len('U-test pvalue = ')
        end_index = text.find('\n', start_index)
        return text[start_index:end_index]

    # Modifying a csv file to add the U-test pvalue
    with open(Path(result_folder, 'Summary', 'Scores training CV.csv', newline='')) as csvfile:
        reader = csv.reader(csvfile)
        with open(Path(result_folder, 'Summary', 'Scores training CV (2).csv'), mode='w', newline='') as new_csvfile:
            writer = csv.writer(new_csvfile)
            for i, row in enumerate(reader):
                # modified values
                if i == 0:
                    row.append('U-test pvalue')
                else:
                    model = row[0]
                    row.append(get_pvalue_from_Boxplot(model))
                writer.writerow(row)
                
    return predictions_dict



def stacked_generalization_time_model():
    """Function to get predictions, weights and AUC of generalized 
    models based on the predictions of the single omic models which 
    were given by the stroke_pipeline function.
    It saves all the results in the same file 'Results' that was used
    to store the predictions of the single omic models.

    Parameters
    ----------

    Returns
    -------
    """
    Y = pd.read_csv("./Stroke/Data/P1/Bcells/y.csv", index_col=0)['0']
    Y.name = 'outcome'
    times = ['P1', 'P2', 'P3', 'Delta']
    
    for time in times:
        print('**********************************************   ' + time + '    **********************************************')
        # Collection of results of single omic models
        ## Initialization
        df_predictions = {}
        for model in ['Lasso', 'Lasso 1SE', 'STABL', 'SS 03', 'SS 05', 'SS 08', 'ElasticNet']:
            df_predictions[model] = pd.DataFrame()
        ## Collecting results
        print('     * collecting the results of the single omic models...')
        for foldername in os.listdir(Path('./Stroke/Results', time)):
            if not foldername.startswith('.'):
                for model in ['Lasso', 'Lasso 1SE', 'STABL', 'SS 03', 'SS 05', 'SS 08', 'ElasticNet']:
                    for file in os.listdir(Path('./Stroke/Results', time, foldername, 'Training CV', model)):
                        if 'csv' in file:
                            new_pred = pd.read_csv(Path('./Stroke/Results', time, foldername, 'Training CV', model, file), index_col=0)
                            new_pred.columns = [foldername.replace('Results', 'predictions'), 'outcome']
                            df_predictions[model] = pd.concat([df_predictions[model], new_pred[[foldername.replace('Results', 'predictions')]]], axis='columns') 
        print('     * Done !')
        
        print('     * collecting the results of the generalized models...')
        # Collection of results of generalized models
        generalized_models_preds = {}
        generalized_models_weights = {}
        for model in ['Lasso', 'Lasso 1SE', 'STABL', 'SS 03', 'SS 05', 'SS 08', 'ElasticNet']:
            print('         -> ' + model)
            generalized_models_preds[model], generalized_models_weights[model] = stacked_multi_omic(df_predictions[model], Y, task_type='binary')
            generalized_models_preds[model] = generalized_models_preds[model]['Stacked Gen. Predictions']
        print('     * Done !')
        
        print('     * Saving Results...')
        # Saving Results
        save_path = Path('./Stroke', 'Results', 'SG Time&Model ', time)
        os.makedirs(save_path, exist_ok = True)
        save_plots(generalized_models_preds, Y, task_type='binary', save_path=save_path)
        for model in ['Lasso', 'Lasso 1SE', 'STABL', 'SS 03', 'SS 05', 'SS 08', 'ElasticNet']:
            generalized_models_weights[model].sort_values('Associated weight', ascending=False).to_csv(Path(save_path, model, 'weights.csv'))
        print('     * Done !')
        
    return


########## MAX PIPELINE ##########

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
    sample_fraction = 0.9,
    random_state=46
)

stablList = [clone(stabl_class),clone(stabl_class).set_params(artificial_type="random_permutation"),
             clone(stabl_class).set_params(base_estimator=clone(logit_en05)),
             clone(stabl_class).set_params(base_estimator=clone(logit_en05),artificial_type="random_permutation")]
stablNames = ["L-KF","L-RP","EN05-KF","EN05-RP"]

outer_splitter = LeaveOneOut()

stability_selection = clone(stabl_class).set_params(artificial_type=None, hard_threshold=0.3)


def run(timePoint,stablIdx):
    data = pd.read_csv("./Sample Data/Stroke/"+timePoint+".csv",index_col=0)
    label = pd.read_csv("./Sample Data/Stroke/Label.csv",index_col=0).iloc[:,0]

    preprocessing = Pipeline(
        steps=[
            ("lif", LowInfoFilter(0.2)),
            ("variance", VarianceThreshold(0.01)),
            ("impute", SimpleImputer(strategy="median")),
            ("std", StandardScaler())
        ]
    )
    # data = pd.DataFrame(
    #     data=preprocessing.fit_transform(data),
    #     index=data.index,
    #     columns=preprocessing.get_feature_names_out()
    # )

    # preprocessing2 = Pipeline(
    #     steps=[
    #         ("std", StandardScaler())
    #     ]
    # )

    dataSTD = pd.DataFrame(
        data=preprocessing.fit_transform(data),
        index=data.index,
        columns=preprocessing.get_feature_names_out()
    )

    resultFolderRoot = "./Results16/V"+timePoint+ "/"
    resultFolder = resultFolderRoot + stablNames[stablIdx]
    resultFolderUnivariate = resultFolderRoot+"/Univariate/"
    os.makedirs("./Results16",exist_ok=True)
    os.makedirs(resultFolderRoot, exist_ok=True)
    os.makedirs(resultFolder, exist_ok=True)
    os.makedirs(resultFolderUnivariate, exist_ok=True)

    if stablIdx == 0:
        vals1 = []
        vals2 = []
        for col in data.columns:
            a,b = mannwhitneyu(data.loc[label == 0,col].to_numpy(),data.loc[label == 1,col].to_numpy())
            vals1.append(a)
            vals2.append(b)

        res = pd.DataFrame(data=[vals1,vals2],index= ["Mann-Whitney U-test","p-value"],columns=data.columns)
        res = res.sort_values(by="p-value",axis=1)
        res.T.to_csv(Path(resultFolderUnivariate + "Mann-WhitneyU-testPval.csv"))
        

        boxplot_features(    list_of_features=res.columns[:10],
        df_X=data[res.columns[:10]],
        y=label,
        show_fig=False,
        export_file=True,
        path = Path(resultFolderUnivariate)
        )


    single_omic_stabl_cv(
    X=data,
    y=label.astype(int),
    outer_splitter=outer_splitter,
    stabl=stablList[stablIdx],
    stability_selection=stability_selection,
    task_type="binary",
    save_path=Path(resultFolder),
    )
    stabl = clone(stablList[stablIdx])
    stabl.fit(dataSTD,label.astype(int))


    save_stabl_results(stabl,resultFolder+"/FinalSTABL/",dataSTD,label,task_type="binary")
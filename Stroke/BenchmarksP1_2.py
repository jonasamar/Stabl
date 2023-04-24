import warnings
warnings.filterwarnings('ignore')
# Libraries
## Basic libraries
import numpy as np
import pandas as pd
from pathlib import Path
import os

from sklearn.model_selection import LeaveOneOut, RepeatedStratifiedKFold, RepeatedKFold
from sklearn.base import clone

from stabl.stabl import Stabl, plot_stabl_path, plot_fdr_graph, save_stabl_results
from stabl.preprocessing import LowInfoFilter, remove_low_info_samples

## Stabl pipelines
from stabl.multi_omic_pipelines import multi_omic_stabl, multi_omic_stabl_cv
from stabl.single_omic_pipelines import single_omic_stabl, single_omic_stabl_cv
from stabl.pipelines_utils import compute_features_table

# Data
## Importing dataset
dataset = pd.read_csv("../Sample Data/Stroke/preprocessed_HT.csv")
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
    data_path = Path('./Data', time, cellpop)
    os.makedirs(data_path, exist_ok=True)
    os.makedirs('./Results', exist_ok=True)
    
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
    
    result_folder = "./Results/" + time + "/" + cellpop + "_Results" 
    
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
    
    from stabl.single_omic_pipelines import single_omic_stabl_cv

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

    os.makedirs(Path(result_folder, "Training-Validation"))
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

    os.makedirs(Path(result_folder, 'Univariate'))

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
                    
for cellpop in ['CD56dimCD16pNKcells', 'CD61pCD41pPLT', 'CD62LnAgedNeutrophils',
                    'CD62LpImmatureNeutrophils', 'CD8Tcm', 'CD8Tem']:
    stroke_pipeline('P1', cellpop)
        
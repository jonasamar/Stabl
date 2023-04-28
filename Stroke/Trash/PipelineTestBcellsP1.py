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
dataset.shape
for column in dataset.columns:
    print(f"{column} values : {dataset[column].unique()}")
    print(f"card({column}) : {len(dataset[column].unique())}")
    print()
# Test 1 : for Bcells
dataset = dataset[dataset['population']=='Bcells*']
dataset['group'][dataset['group']=='No']=0
dataset['group'][dataset['group']=='Yes']=1
#dataset
# P1
data_path = Path('./Data', './BCells_P1')
os.makedirs(data_path, exist_ok=True)
os.makedirs('./Results', exist_ok=True)
P1_dataset = dataset[dataset['time']=='P1']
## Multivariate Analysis
### Dataset
P1_dict_x = {}
P1_dict_y = {}
for sample in dataset['sampleID']:
    P1_dict_x[sample] = {}
    for feature in dataset['reagent'].unique():
        mask = (P1_dataset['sampleID']==sample) & (P1_dataset['reagent']==feature)
        P1_dict_x[sample][feature] = float(P1_dataset[mask]['feature'])
    P1_dict_y[sample] = P1_dataset[P1_dataset['sampleID']==sample]['group'].iloc[0]
        
pd.DataFrame(P1_dict_x).T.to_csv(Path(data_path, "X_P1_Bcells.csv"), index=True)
pd.DataFrame([P1_dict_y]).T.to_csv(Path(data_path, "y_P1_Bcells.csv"), index=True)
X = pd.read_csv(Path(data_path, "X_P1_Bcells.csv"), index_col=0)
y = pd.read_csv(Path(data_path, "y_P1_Bcells.csv"), index_col=0).iloc[:, 0]
y.name = None
### Result folder name
result_folder = "./Results/Results P1 Bcells Kfold"
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

#outer_splitter = LeaveOneOut()
#outer_splitter = RepeatedStratifiedKFold(n_splits=len(X), n_repeats=20, random_state=42)
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
## Univariate
from scipy.stats import spearmanr
import numpy as np

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
        SpearmanPvalue[:5].index,
        X,
        y,
        show_fig=False,
        export_file=True,
        path=Path(result_folder, 'Univariate'))
### Rearrangement of results
import shutil

# Source and destination paths
for model in ["STABL", "Lasso", "Lasso 1SE", "ElasticNet", "SS 03", "SS 05", "SS 08"]:
    src_folder = Path(result_folder, 'Training CV', model)
    dst_folder = Path(result_folder, 'Summary')

    # Loop over the files in the source folder
    for filename in os.listdir(src_folder):
        if "Boxplot" in filename:
            src_file = os.path.join(src_folder, filename)
            dst_file = os.path.join(dst_folder, filename)
            shutil.copy(src_file, dst_file)
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


import warnings
warnings.filterwarnings('ignore')
# Libraries
## Basic libraries
import numpy as np
import pandas as pd
from pathlib import Path

from sklearn.model_selection import RepeatedStratifiedKFold
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
dataset
# PO
PO_dataset = dataset[dataset['time']=='P1']
## Multivariate Analysis
### Dataset
PO_dict_x = {}
PO_dict_y = {}
for sample in dataset['sampleID']:
    PO_dict_x[sample] = {}
    for feature in dataset['reagent'].unique():
        mask = (PO_dataset['sampleID']==sample) & (PO_dataset['reagent']==feature)
        PO_dict_x[sample][feature] = float(PO_dataset[mask]['feature'])
    PO_dict_y[sample] = PO_dataset[PO_dataset['sampleID']==sample]['group'].iloc[0]
        
X_PO = pd.DataFrame(PO_dict_x).T 
y_PO = pd.DataFrame([PO_dict_y]).T 
### Result folder name
result_folder = "./Results PO Bcells"
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

outer_splitter = RepeatedStratifiedKFold(n_splits=5, n_repeats=20, random_state=42)
predictions_dict = single_omic_stabl_cv(
    X=X_PO,
    y=y_PO,
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
    X_train=X_PO,
    y_train=y_PO,
    X_test=None,
    y_test=None,
    task_type="binary")

features_table.to_csv(Path(result_folder, "Training-Validation", "Table of features.csv"))
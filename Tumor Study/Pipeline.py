import warnings
warnings.filterwarnings('ignore')
# Libraries
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import zscore
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.base import clone
from sklearn.linear_model import Lasso

from stabl.stabl import Stabl, plot_stabl_path, plot_fdr_graph, save_stabl_results, export_stabl_to_csv
from stabl.preprocessing import LowInfoFilter, remove_low_info_samples

from stabl.multi_omic_pipelines import multi_omic_stabl, multi_omic_stabl_cv, late_fusion_lasso_cv
from stabl.single_omic_pipelines import single_omic_stabl, single_omic_stabl_cv
from stabl.pipelines_utils import compute_features_table

# Data

## 1st Cohort
Val_Celldensities = pd.read_csv('./Tumor Study/DataValidation/Val_celldensities.csv', index_col=0)
Val_Function = pd.read_csv('./Tumor Study/DataValidation/Val_functional.csv', index_col=0)
Val_Metavariables = pd.read_csv('./Tumor Study/DataValidation/Val_metavariables.csv', index_col=0)
Val_Neighborhood = pd.read_csv('./Tumor Study/DataValidation/Val_neighborhood.csv', index_col=0)

val_data = {
    'Val_Celldensities': Val_Celldensities,
    'Val_Function': Val_Function,
    'Val_Metavariables': Val_Metavariables,
    'Val_Neighborhood': Val_Neighborhood
}

### Z-scoring 1st Cohort
for data_name, data_frame in val_data.items():
    numeric_columns = data_frame.select_dtypes(include=['float64', 'int64']).columns
    val_data[data_name][numeric_columns] = val_data[data_name][numeric_columns].apply(zscore)

Val_y = pd.read_csv('./Tumor Study/DataValidation/Val_outcome.csv',index_col=0)
Val_y['site'] = 'Stanford'

## 2nd Cohort
UOP_Celldensities = pd.read_csv('./Tumor Study/DataTraining/UOPfinal_celldensities.csv', index_col=0)
UOP_Function = pd.read_csv('./Tumor Study/DataTraining/UOPfinal_functional.csv', index_col=0)
UOP_Metavariables = pd.read_csv('./Tumor Study/DataTraining/UOPfinal_metavariables.csv', index_col=0)
UOP_Neighborhood = pd.read_csv('./Tumor Study/DataTraining/UOPfinal_neighborhood.csv', index_col=0)

UOP_data = {
    'UOP_Celldensities': UOP_Celldensities,
    'UOP_Function': UOP_Function,
    'UOP_Metavariables': UOP_Metavariables,
    'UOP_Neighborhood': UOP_Neighborhood
}

### Z-scoring 2nd Cohort
for data_name, data_frame in UOP_data.items():
    numeric_columns = data_frame.select_dtypes(include=['float64', 'int64']).columns
    UOP_data[data_name][numeric_columns] = UOP_data[data_name][numeric_columns].apply(zscore)

UOP_y = pd.read_csv('./Tumor Study/DataTraining/UOPfinal_outcome.csv',index_col=0)
UOP_y['site'] = 'UOP'

## Concatenating the two cohorts
X_Celldensities = pd.concat([Val_Celldensities, UOP_Celldensities])
X_Function = pd.concat([Val_Function, UOP_Function])
X_Metavariables = pd.concat([Val_Metavariables, UOP_Metavariables])
X_Neighborhood = pd.concat([Val_Neighborhood, UOP_Neighborhood])
y = pd.concat([Val_y, UOP_y])
y['patient_id'] = y.index.str.split('_').str.get(0)

data = {
    'Celldensities': X_Celldensities,
    'Function': X_Function,
    'Metavariables': X_Metavariables,
    'Neighborhood': X_Neighborhood,
    'Outcome': y
}

features = {
    'Celldensities': X_Celldensities,
    'Function': X_Function,
    'Metavariables': X_Metavariables,
    'Neighborhood': X_Neighborhood
}

outcome = y['grade'] - 1 # instead of 1-2 -> 0-1 for the grade

# Pipeline    
stabl = Stabl(
    lambda_name='C',
    lambda_grid=np.linspace(0.01, 5, 10),
    n_bootstraps=1000,
    artificial_type="random_permutation",
    artificial_proportion=1.,
    replace=False,
    fdr_threshold_range=np.arange(0.2, 1, 0.01),
    sample_fraction=.5,
    random_state=42
 )

outer_splitter = RepeatedStratifiedKFold(n_splits=5, n_repeats=20, random_state=1)

stability_selection = clone(stabl).set_params(artificial_type=None, hard_threshold=0.5)

# Multi-omic Training-CV

predictions_dict = multi_omic_stabl_cv(
    data_dict=features,
    y=outcome,
    outer_splitter=outer_splitter,
    stabl=stabl,
    stability_selection=stability_selection,
    task_type="binary",
    save_path=" ./Tumor Study/Results"
)
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
Val_Celldensities = pd.read_csv('DataValidation/Stanford_celldensities_median.csv', index_col=0)
Val_Function = pd.read_csv('DataValidation/Stanford_functional_median.csv', index_col=0)
Val_Metavariables = pd.read_csv('DataValidation/Stanford_metavariables_median.csv', index_col=0)
Val_Neighborhood = pd.read_csv('DataValidation/Stanford_neighborhood_median.csv', index_col=0)

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

Val_y = pd.read_csv('DataValidation/Val_outcome.csv',index_col=0)
Val_y['site'] = 'Stanford'

## 2nd Cohort
UOP_Celldensities = pd.read_csv('DataTraining/UOP_celldensities_median.csv', index_col=0)
UOP_Function = pd.read_csv('DataTraining/UOP_functional_median.csv', index_col=0)
UOP_Metavariables = pd.read_csv('DataTraining/UOP_metavariables_median.csv', index_col=0)
UOP_Neighborhood = pd.read_csv('DataTraining/UOP_neighborhood_median.csv', index_col=0)

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

UOP_y = pd.read_csv('DataTraining/UOPfinal_outcome.csv',index_col=0)
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

## Splitting the Data
unique_patients = pd.DataFrame(y['patient_id'].unique(), columns=['patient_id'])
unique_patients = unique_patients.merge(y, on='patient_id', how = 'left') 
unique_patients = unique_patients.drop_duplicates(subset=['patient_id', 'grade', 'site'])

train_df, val_df = train_test_split(unique_patients, test_size=0.25, stratify=unique_patients[['site', 'grade']])

print("Training set shape:", train_df.shape)
print("Validation set shape:", val_df.shape)
train_indices = y[y['patient_id'].isin(train_df['patient_id'])].index
test_indices = y[y['patient_id'].isin(val_df['patient_id'])].index

train_data_dict = {}
test_data_dict = {}

for key, df in data.items():
    train_df = df.loc[train_indices]  # Select rows from the dataframe based on train indices
    test_df = df.loc[test_indices] # Drop rows from the dataframe based on train indices
    
    train_data_dict[key] = train_df
    test_data_dict[key] = test_df


train_outcome = train_data_dict.pop('Outcome')
train_outcome = train_outcome.grade-1 # So that we get values that are 0 and 1 instead of 1 and 2
test_outcome = test_data_dict.pop('Outcome')
test_outcome = test_outcome.grade-1 # So that we get values that are 0 and 1 instead of 1 and 2

# Pipeline    

## Multi-omic Training-CV
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

predictions_dict = multi_omic_stabl_cv(
    data_dict=train_data_dict,
    y=train_outcome,
    outer_splitter=outer_splitter,
    stabl=stabl,
    stability_selection=stability_selection,
    task_type="binary",
    save_path="../Tumor Study/Results_with_split"
)

## Multi-omic Validation
stabl_multi = Stabl(
    lambda_grid=np.linspace(0.01, 5, 30),
    n_bootstraps=1000,
    artificial_proportion=1.,
    artificial_type="random_permutation",
    hard_threshold=None,
    replace=False,
    fdr_threshold_range=np.arange(0.2, 1, 0.01),
    sample_fraction=.7,
    random_state=42
)

stability_selection = clone(stabl_multi).set_params(artificial_type=None, hard_threshold=.3)

predictions_dict = multi_omic_stabl(
    data_dict=train_data_dict,
    y=train_outcome,
    stabl=stabl_multi,
    stability_selection=stability_selection,
    task_type="binary",
    save_path="../Tumor Study/Results_with_split",
    X_test = test_data_dict,
    y_test = test_outcome
)

# Table Features
selected_features_dict = dict()
for model in ["STABL", "EF Lasso", "SS 03", "SS 05", "SS 08"]:
    path = Path("../Tumor Study/Results_with_split", "Training-Validation", f"{model} coefficients.csv")
    try:
        selected_features_dict[model] = list(pd.read_csv(path, index_col=0).iloc[:, 0].index)
    except:
        selected_features_dict[model] = []
        
features_table = compute_features_table(
    selected_features_dict,
    X_train=pd.concat(train_data_dict.values(), axis=1),
    y_train=train_outcome,
    X_test = test_data_dict,
    y_test = test_outcome,
    task_type="binary"
)

features_table.to_csv(Path("../Tumor Study/Results_with_split", "Training-Validation", "Table of features.csv"))
import warnings
warnings.filterwarnings('ignore')
# Libraries
## Basic libraries
import numpy as np
import pandas as pd
from pathlib import Path

from sklearn.model_selection import GroupShuffleSplit
from sklearn.base import clone 

from stabl.stabl import Stabl, plot_stabl_path, plot_fdr_graph, save_stabl_results
from stabl.preprocessing import LowInfoFilter, remove_low_info_samples

## Stabl pipelines
from stabl.multi_omic_pipelines import multi_omic_stabl, multi_omic_stabl_cv
from stabl.single_omic_pipelines import single_omic_stabl, single_omic_stabl_cv
from stabl.pipelines_utils import compute_features_table
# Data
# Importing the input dataframe
X = pd.read_csv("../Sample Data/CFRNA/cfrna_dataFINAL.csv", index_col=0)

# Importing patients' ID
IDs = pd.read_csv("../Sample Data/CFRNA/ID.csv", index_col=0)

# Importing the Preeclampsia outcome
y = pd.read_csv("../Sample Data/CFRNA/all_outcomes.csv", index_col=0)

X = remove_low_info_samples(X)  # Removing samples without any information
X = X.apply(lambda x: np.log2(x+1))  # Applying the log2(x+1) transformation

IDs = IDs.loc[X.index]
y = y.loc[X.index].Preeclampsia
# Single Omic in Training-CV
stabl = Stabl(
    lambda_grid=np.linspace(0.01, 5, 10),
    n_bootstraps=250,
    artificial_type="random_permutation",
    artificial_proportion=.5,
    replace=False,
    fdr_threshold_range=np.arange(0.1, 1, 0.01),
    sample_fraction=.5,
    backend_multi="threading",
    random_state=42
 )

outer_splitter = GroupShuffleSplit(n_splits=100, test_size=.2, random_state=2)

stability_selection = clone(stabl).set_params(artificial_type=None, hard_threshold=0.3)
result_folder = "./Results CFRNA"
single_omic_stabl_cv(
    X=X,
    y=y.astype(int),
    outer_splitter=outer_splitter,
    stabl=stabl,
    stability_selection=stability_selection,
    task_type="binary",
    save_path=Path(result_folder),
    outer_groups=IDs,
)
# Single Omic Training
stabl = Stabl(
    lambda_grid=np.linspace(0.01, 5, 30),
    n_bootstraps=1000,
    artificial_type="random_permutation",
    artificial_proportion=.5,
    replace=False,
    fdr_threshold_range=np.arange(0.1, 1, 0.01),
    sample_fraction=.5,
    backend_multi="threading",
    random_state=42
 )
stability_selection = clone(stabl).set_params(artificial_type=None, hard_threshold=0.3)
single_omic_stabl(
    X=X,
    y=y.astype(int),
    stabl=stabl,
    stability_selection=stability_selection,
    task_type="binary",
    save_path=Path(result_folder)
)
# Table of features
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
    y_train=y.astype(int),
    task_type="binary")
features_table.to_csv(Path(result_folder, "Training-Validation", "Table of features.csv"))
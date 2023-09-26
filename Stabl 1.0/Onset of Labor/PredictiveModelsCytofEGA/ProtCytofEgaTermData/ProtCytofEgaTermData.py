import warnings 
warnings.filterwarnings('ignore')

#Basic libraries
import os
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import GroupShuffleSplit, RepeatedStratifiedKFold, LeaveOneOut, LeaveOneGroupOut
from sklearn.base import clone
from scipy.stats import mannwhitneyu, spearmanr
from stabl.visualization import scatterplot_features, boxplot_features
from stabl.stabl import Stabl, save_stabl_results

from sklearn.linear_model import LassoCV, LogisticRegressionCV, LogisticRegression, LinearRegression, ElasticNetCV, Lasso

#STABL pipelines
from stabl.multi_omic_pipelines import multi_omic_stabl, multi_omic_stabl_cv
from stabl.single_omic_pipelines import single_omic_stabl, single_omic_stabl_cv

#Preprocessing functions
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold
from stabl.preprocessing import LowInfoFilter, remove_low_info_samples

#Import Data
train_data_dict = {
	'GA': pd.read_csv('../ProtCytofEgaTermData/GA_term.csv',index_col=0),
	'Proteomics': pd.read_csv('../ProtCytofEgaTermData/Proteomics_term.csv',index_col=0),
	'CYTOF': pd.read_csv('../ProtCytofEgaTermData/Cytof_term.csv',index_col=0)
}

y = pd.read_csv('../ProtCytofEgaTermData/DOS_term.csv',index_col=0).iloc[:,0]


logit_en = LogisticRegression(penalty='l1', max_iter=int(1e6), solver='liblinear', class_weight='balanced')

stabl = Stabl(base_estimator=clone(logit_en),
	lambda_name='C',
	lambda_grid=list(np.linspace(0.01, 1, 30)),
	n_bootstraps=1000,
	artificial_type='random_permutation',
	artificial_proportion=1.,
	sample_fraction=0.5,
	replace=False,
	fdr_threshold_range=list(np.arange(0., 1., .01)),
	sample_weight_bootstrap=None,
	bootstrap_threshold=1e-5,
	backend_multi='threading',
	verbose=0,
	n_jobs=-1,
	random_state=42)

stability_selection = clone(stabl).set_params(artificial_type=None, hard_threshold=0.3)

preprocessing = Pipeline(
	steps=[
		('lif', LowInfoFilter(0.2)),
		('variance', VarianceThreshold(0.0)),
		('impute', SimpleImputer(strategy='median')),
		('std', StandardScaler())
	])


#Import Validation Data
X_test = {
	'GA': pd.read_csv('../ProtCytofEgaTermData/GA_preterm.csv',index_col=0),
	'Proteomics': pd.read_csv('../ProtCytofEgaTermData/Proteomics_preterm.csv',index_col=0),
	'CYTOF': pd.read_csv('../ProtCytofEgaTermData/Cytof_preterm.csv',index_col=0)
}

# Columns order verifications
for omic_name in X_test.keys():
    X_test[omic_name] = X_test[omic_name][train_data_dict[omic_name].columns.tolist()]
    columns_match = X_test[omic_name].columns.equals(train_data_dict[omic_name].columns)
    print(omic_name)
    if columns_match:
        print("The columns are ordered the same way.")
    else:
        print("The columns are not ordered the same way.")

for omic_name, X_omic in X_test.items():
	all_data = dict() #NEW
	if set(train_data_dict[omic_name].columns) != set(X_omic.columns):
		print('>>> !!! BE AWARE THAT YOUR TRAINING AND  VALIDATIONS ' + omic_name + ' FEATURES ARE NOT EXACTLY THE SAME ! Consequently the validation pipeline and univariate analysis will be run with the intersection of these features !!! <<<')
		features = list(set(train_data_dict[omic_name].columns).intersection(set(X_omic.columns)))
		X_test[omic_name] = X_omic[features]
		train_data_dict[omic_name] = train_data_dict[omic_name][features]
		all_data[omic_name] = pd.concat([train_data_dict[omic_name], X_omic[features]], axis=0) #NEW
	else: 
		all_data[omic_name] = pd.concat([train_data_dict[omic_name], X_omic], axis=0) #NEW

y_test = pd.read_csv('../ProtCytofEgaTermData/DOS_preterm.csv',index_col=0).iloc[:,0]
all_outcomes = pd.concat([y, y_test], axis=0)

multi_omic_stabl(
	train_data_dict,
	y.astype(int),
	stabl=stabl,
	stability_selection=stability_selection,
	task_type='regression',
	save_path='../ProtCytofEgaTermData/Results',
	X_test=pd.concat(X_test.values(), axis=1),
	y_test=y_test.astype(int),
	preprocessing=preprocessing)


#Univariate
os.makedirs('../ProtCytofEgaTermData/Results/Univariate', exist_ok=True)
for omic in all_data.keys():
	os.makedirs('../ProtCytofEgaTermData/Results/Univariate/'+omic, exist_ok=True)
	X = all_data[omic]
	Spearmancorr = {}
	features = X.columns
	for feature in features:
		corr, pval = spearmanr(X[feature], all_outcomes)
		Spearmancorr[feature] = [corr, pval]

	SpearmanPvalue = pd.DataFrame(Spearmancorr).T
	SpearmanPvalue.columns = ['Spearman corr', 'pvalue']
	SpearmanPvalue.sort_values('pvalue', inplace=True)
	SpearmanPvalue.to_csv('../ProtCytofEgaTermData/Results/Univariate/'+omic+'/SpearmanCorrelationsPval.csv', index=True)

	scatterplot_features(
		SpearmanPvalue[:10].index,
		X,
		all_outcomes,
		show_fig=False,
		export_file=True,
		path='../ProtCytofEgaTermData/Results/Univariate/'+omic)
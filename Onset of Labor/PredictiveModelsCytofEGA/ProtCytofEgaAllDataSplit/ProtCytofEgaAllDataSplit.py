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
from stabl.stacked_generalization import stacked_multi_omic

#Preprocessing functions
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import train_test_split

from stabl.preprocessing import LowInfoFilter, remove_low_info_samples

#Import Data
X_ga = pd.read_csv('../ProtCytofEgaAllDataSplit/GA.csv',index_col=0)
X_cytof = pd.read_csv('../ProtCytofEgaAllDataSplit/Cytof.csv',index_col=0)
X_prot = pd.read_csv('../ProtCytofEgaAllDataSplit/Proteomics.csv',index_col=0)

train_data_dict = {
	'CYTOF': X_cytof,
	'GA': X_ga,
	'Proteomics': X_prot
}

X_test = dict()

# Splitting data
train_idx, test_idx = train_test_split(X_cytof.index, test_size=0.2, random_state=42)
for omic_name in train_data_dict.keys():
	print('-------- ' + omic_name + ' --------')
	X_omic = train_data_dict[omic_name]
	X_test[omic_name] = X_omic.loc[test_idx]
	train_data_dict[omic_name] = X_omic.loc[train_idx]
	print(X_test[omic_name].head())
	print('test shape : '+ str(X_test[omic_name].shape))
	print(train_data_dict[omic_name].head())
	print('train shape : '+ str(train_data_dict[omic_name].shape))

print('-------- ' + 'outcomes' + ' --------')
y = pd.read_csv('../ProtCytofEgaAllDataSplit/DOS.csv',index_col=0).loc[train_idx].iloc[:,0]
y_test = pd.read_csv('../ProtCytofEgaAllDataSplit/DOS.csv',index_col=0).loc[test_idx].iloc[:,0]
print(y.head())
print('train shape : '+ str(len(y)))
print(y_test.head())
print('test shape : '+ str(len(y_test)))



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

# Here we concatenate all the data (features and outcomes)
# This step is usefull when there are training and validation data (in this script we only create these variables for univariate analysis and final model)
all_data = train_data_dict
all_outcomes = y

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

all_outcomes = pd.concat([y, y_test], axis=0)

multi_omic_stabl(
	train_data_dict,
	y.astype(int),
	stabl=stabl,
	stability_selection=stability_selection,
	task_type='regression',
	save_path='../ProtCytofEgaAllDataSplit/Results',
	X_test=pd.concat(X_test.values(), axis=1),
	y_test=y_test.astype(int),
	preprocessing=preprocessing)


#Univariate
os.makedirs('../ProtCytofEgaAllDataSplit/Results/Univariate', exist_ok=True)
for omic in all_data.keys():
	os.makedirs('../ProtCytofEgaAllDataSplit/Results/Univariate/'+omic, exist_ok=True)
	X = all_data[omic]
	Spearmancorr = {}
	features = X.columns
	for feature in features:
		corr, pval = spearmanr(X[feature], all_outcomes)
		Spearmancorr[feature] = [corr, pval]

	SpearmanPvalue = pd.DataFrame(Spearmancorr).T
	SpearmanPvalue.columns = ['Spearman corr', 'pvalue']
	SpearmanPvalue.sort_values('pvalue', inplace=True)
	SpearmanPvalue.to_csv('../ProtCytofEgaAllDataSplit/Results/Univariate/'+omic+'/SpearmanCorrelationsPval.csv', index=True)

	scatterplot_features(
		SpearmanPvalue[:10].index,
		X,
		all_outcomes,
		show_fig=False,
		export_file=True,
		path='../ProtCytofEgaAllDataSplit/Results/Univariate/'+omic)
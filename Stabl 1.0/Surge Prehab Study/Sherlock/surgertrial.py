import warnings 
warnings.filterwarnings('ignore')

#Basic libraries
import os
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import GroupShuffleSplit, RepeatedStratifiedKFold, LeaveOneOut
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
X = pd.read_csv('/Users/jonasamar/Stabl/Surge Prehab Study/prehab_preprocessed_ratioIDX_BL.csv',index_col=0)

y = pd.read_csv('/Users/jonasamar/Stabl/Surge Prehab Study/outcome_file.csv',index_col=0).iloc[:,0]


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
		('variance', VarianceThreshold(0.1)),
		('impute', SimpleImputer(strategy='median')),
		('std', StandardScaler())
	])


outer_splitter = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=42)
# Here we concatenate all the data (features and outcomes)
# This step is usefull when there are training and validation data (in this script we only create these variables for univariate analysis and final model)
all_data = X
all_outcomes = y

#single_omic_stabl_cv(
#	X=X,
#	y=y.astype(int),
#	outer_splitter=outer_splitter,
#	stabl=stabl,
#	stability_selection=stability_selection,
#	task_type='binary',
#	save_path='../surgertrial/Results',
#	preprocessing=preprocessing)


#Univariate
os.makedirs('./Surge Prehab Study/Results/Univariate', exist_ok=True)
vals1 = []
vals2 = []
for col in all_data.columns:
	a,b = mannwhitneyu(all_data.loc[all_outcomes == 0,col].dropna().to_numpy(),all_data.loc[all_outcomes == 1,col].dropna().to_numpy())
	vals1.append(a)
	vals2.append(b)

res = pd.DataFrame(data=[vals1,vals2],index= ['Mann-WhitneyU-test','p-value'],columns=X.columns)
res = res.sort_values(by='p-value',axis=1)
res.T.to_csv('./Surge Prehab Study/Results/Univariate/Mann-WhitneyU-testPval.csv')

boxplot_features(
	list_of_features=res.columns[:10],
	df_X=all_data[res.columns[:10]],
	y=all_outcomes,
	show_fig=False,
	export_file=True,
	path ='./Surge Prehab Study/Results/Univariate'
)

#Final STABL
#finalstabl = clone(stabl)
#X_STD = pd.DataFrame(
#	data=preprocessing.fit_transform(all_data),
#	index=all_data.index,
#	columns=preprocessing.get_feature_names_out()
#)
#finalstabl.fit(X_STD, all_outcomes.astype(int))

#save_stabl_results(finalstabl,'../surgertrial/Results'+'/FinalSTABL/',X_STD, all_outcomes.astype(int),task_type='binary')

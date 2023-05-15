import warnings 
warnings.filterwarnings('ignore')

#Basic libraries
import os
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import GroupShuffleSplit, RepeatedStratifiedKFold, LeaveOneOut
from sklearn.base import clone
from scipy.stats import mannwhitneyu, pearsonr
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
X = pd.read_csv('./COVD19test/Proteomics.csv',index_col=0)

y = pd.read_csv('./COVD19test/Mild&ModVsSevere.csv',index_col=0).iloc[:,0]


logit_en = LogisticRegression(penalty='elasticnet', l1_ratio = 1.0, max_iter=int(1e6), solver='saga', class_weight='balanced')

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
		('variance', VarianceThreshold(0.01)),
		('impute', SimpleImputer(strategy='median')),
		('std', StandardScaler())
	])

X_STD = pd.DataFrame(
	data=preprocessing.fit_transform(X),
	index=X.index,
	columns=preprocessing.get_feature_names_out()
)

outer_splitter = RepeatedStratifiedKFold(n_splits=5, n_repeats=20, random_state=42)

single_omic_stabl_cv(
	X=X,
	y=y.astype(int),
	outer_splitter=outer_splitter,
	stabl=stabl,
	stability_selection=stability_selection,
	task_type='binary',
	save_path='./COVD19test/Results'
)

#Univariate
os.makedirs('./{foldername}/Results/Univariate', exist_ok=True)
vals1 = []
vals2 = []
for col in X.columns:
	a,b = mannwhitneyu(X.loc[y == 0,col].to_numpy(),X.loc[y == 1,col].to_numpy())
	vals1.append(a)
	vals2.append(b)

res = pd.DataFrame(data=[vals1,vals2],index= ['Mann-WhitneyU-test','p-value'],columns=X.columns)
res = res.sort_values(by='p-value',axis=1)
res.T.to_csv('./COVD19test/Results/Univariate/' + 'Mann-WhitneyU-testPval.csv')

boxplot_features(
	list_of_features=res.columns[:10],
	df_X=X[res.columns[:10]],
	y=y,
	show_fig=False,
	export_file=True,
	path ='./COVD19test/Results/Univariate'
)

#Final STABL
finalstabl = clone(stabl)
finalstabl.fit(X_STD,y.astype(int))

save_stabl_results(finalstabl,'./COVD19test/Results'+'/FinalSTABL/',X_STD,y,task_type='binary')

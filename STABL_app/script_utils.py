
import os
from pathlib import Path
import re
from subwindows import show_message

def python_script(foldername, X_file, y_col, y_file, l1_ratio, artificial_type, sample_fraction, replace, random_state, preprocess, outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size):
    if has_special_chars_or_spaces(foldername) or len(foldername) == 0:
        show_message("Error", "Your STABL Run Name contains undesired characters or spaces or is empty, please chose another name.")
    elif X_file[-4:] != ".csv":
        show_message("Error", "Your datafile name doesn't correspond to a csv file name. Please convert it to a csv file before creating your python script.")
    elif y_file[-4:] != ".csv":
        show_message("Error", "Your outcome file name doesn't correspond to a csv file name. Please convert it to a csv file before creating your python script.")
    elif len(X_file) < 5:
        show_message("Error", "Your datafile name is incorrect. It should be a csv file and the name should contain 5 characters or more.")
    elif len(y_file) < 5:
        show_message("Error", "Your outcome file name is incorrect. It should be a csv file and the name should contain 5 characters or more.")
    elif y_col == "" and y_file == "":
        show_message("Error", "You have not specified where to find the outcomes you want to predict. Please, specify the column of your dataset corresponding to the outcomes and/or specify the name of the csv file containing your outcomes.")
    elif not artificial_type in ["random_permutation", "knockoff"]:
        show_message("Error", "The artificial type you selected is not recognized. Make sure it is either random_permutation or knockoff.")
    elif not outersplitter in ['LeaveOneOut', 'RepeatedStratifiedKFold', 'GroupShuffleSplit']:
        show_message("Error", "The outer splitter you have selected is not recognised. Please chose between:\n\t*LeaveOneOut\n\t*RepeatedStratifiedKFold\n\t*GroupShuffleSplit")
    else :
        os.makedirs(foldername)
        with open(Path(foldername, foldername + '.py'), 'w') as fpy:
            # TO DO write the python file to run STABL the way it is asked
            import_lib(fpy)
            import_data(fpy, X_file, y_col, y_file)
            stabl_class(fpy, l1_ratio, artificial_type, sample_fraction, replace, random_state)
            if preprocess:
                preprocessing(fpy)
            outer_splitter(fpy, outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size)
            pipeline(fpy)
            univariate_analysis(fpy)
            final_stabl(fpy, preprocess)
            fpy.close()
        with open(Path(foldername, foldername + '.sbatch'), 'w') as fsbatch:
            # TO DO write the sbatch file to run the python script
            fsbatch.write("Test")
            fsbatch.close()
        if y_col == "":
            show_message("Warning", "You have not specified the column of your datafile containing your outcomes :\n\n\t* If there is no column corresponding to your outcomes in this file continue\n\n\t* If there is a column corresponding to your outcomes in your datafile please specify it\n(you'll need to fill the text box 'Outcome column' and then delete the folder that has just been created with your python script and sbatch file and finally clic on create)\n\nMake sure there is no column with your outcome in the data file otherwise you won't get the expected results.")
        

def has_special_chars_or_spaces(input_string):
    pattern = re.compile('[^A-Za-z0-9]+') 
    return bool(pattern.search(input_string))

def import_lib(fpy):
    """
    Import the necessary libraries to run any stabl pipeline 
    """
    fpy.write("import warnings \nwarnings.filterwarnings('ignore')\n")
    fpy.write("\n")
    fpy.write("#Basic libraries\n")
    fpy.write("import os\n")
    fpy.write("import numpy as np\n")
    fpy.write("import pandas as pd\n")
    fpy.write("from pathlib import Path\n")
    fpy.write("from sklearn.model_selection import GroupShuffleSplit, RepeatedStratifiedKFold, LeaveOneOut\n")
    fpy.write("from sklearn.base import clone\n")
    fpy.write("from scipy.stats import mannwhitneyu\n")
    fpy.write("from stabl.visualization import scatterplot_features, boxplot_features\n")
    fpy.write("from stabl.stabl import Stabl, plot_stabl_path, plot_fdr_graph, save_stabl_results\n")
    fpy.write("from stabl.preprocessing import LowInfoFilter, remove_low_info_samples\n")
    fpy.write("\n")
    fpy.write("from sklearn.linear_model import LassoCV, LogisticRegressionCV, LogisticRegression, LinearRegression, ElasticNetCV, Lasso\n")
    fpy.write("\n")
    fpy.write("#STABL pipelines\n")
    fpy.write("from stabl.multi_omic_pipelines import multi_omic_stabl, multi_omic_stabl_cv\n")
    fpy.write("from stabl.single_omic_pipelines import single_omic_stabl, single_omic_stabl_cv\n")
    fpy.write("from stabl.pipelines_utils import compute_features_table\n")   
    fpy.write("\n") 
    fpy.write("#Preprocessing functions\n") 
    fpy.write("from sklearn.impute import SimpleImputer\n")
    fpy.write("from sklearn.pipeline import Pipeline\n")
    fpy.write("from sklearn.preprocessing import StandardScaler\n")
    fpy.write("from sklearn.feature_selection import VarianceThreshold\n")
    fpy.write("from stabl.preprocessing import LowInfoFilter\n")
    fpy.write("\n")
    
def import_data(fpy, X_file, y_col, y_file):
    fpy.write("#Import Data\n")
    fpy.write(f"X = pd.read_csv('./{X_file}',index_col=0)\n")
    if (y_file != "") and (y_col == ""):
        fpy.write(f"y = pd.read_csv('./{y_file}',index_col=0).iloc[:,0]\n")
        fpy.write("\n")
    elif (y_file == "") and (y_col != ""):
        fpy.write(f"y = X[{y_col}]\n")
        fpy.write(f"X.drop({y_col}, axis=1, inplace=True)\n")
        fpy.write("\n")
    elif (y_file != "") and (y_col != ""):
        fpy.write(f"y = pd.read_csv('./{y_file}',index_col=0).iloc[:,0]\n")
        fpy.write(f"X.drop('{y_col}', axis=1, inplace=True)\n")
        fpy.write("\n")
    else :
        show_message("Error", "Cannot import your data because we don't know where your outcomes are. You need to fill at least one of the two text boxes ('Outome column' or 'Outcome file')")
        

def stabl_class(fpy, l1_ratio, artificial_type, sample_fraction, replace, random_state):
    fpy.write("\n")
    fpy.write(f"logit_en = LogisticRegression(penalty='elasticnet', l1_ratio = {l1_ratio}, max_iter=int(1e6), solver='saga', class_weight='balanced')\n")
    fpy.write("\n")
    fpy.write(f"stabl = Stabl(base_estimator=clone(logit_en),\n\tlambda_name='C',\n\tlambda_grid=list(np.linspace(0.01, 1, 30)),\n\tn_bootstraps=1000,\n\tartificial_type='{artificial_type}',\n\tartificial_proportion=1.,\n\tsample_fraction={sample_fraction},\n\treplace={replace},\n\tfdr_threshold_range=list(np.arange(0., 1., .01)),\n\tsample_weight_bootstrap=None,\n\tbootstrap_threshold=1e-5,\n\tbackend_multi='threading',\n\tverbose=0,\n\tn_jobs=-1,\n\trandom_state={random_state})\n")
    fpy.write("\n")
    fpy.write("stability_selection = clone(stabl).set_params(artificial_type=None, hard_threshold=0.3)\n")
    
def preprocessing(fpy):
    fpy.write("\n")
    fpy.write("preprocessing = Pipeline(\n\tsteps=[\n\t\t('lif', LowInfoFilter(0.2)),\n\t\t('variance', VarianceThreshold(0.01)),\n\t\t('impute', SimpleImputer(strategy='median')),\n\t\t('std', StandardScaler())\n\t])\n")
    fpy.write("\n")
    fpy.write("X_STD = pd.DataFrame(\n\tdata=preprocessing.fit_transform(X),\n\tindex=X.index,\n\tcolumns=preprocessing.get_feature_names_out()\n)\n")
    

def outer_splitter(fpy, outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size):
    fpy.write("\n")
    fpy.write(f"outer_splitter = {outersplitter}(")
    if outersplitter == 'LeaveOneOut':
        fpy.write(")\n")
    elif outersplitter == 'GroupShuffleSplit':
        if test_size > train_size: 
            fpy.write(f"n_splits={n_splits}, test_size={test_size}, random_state={cv_rd})\n")
        else:
            fpy.write(f"n_splits={n_splits}, train_size={train_size}, random_state={cv_rd})\n")
    elif outersplitter == 'RepeatedStratifiedKFold':
        fpy.write(f"n_splits={n_splits}, n_repeats={n_repeat}, random_state={cv_rd})\n")

def pipeline(fpy):
    fpy.write("\n")
    fpy.write("single_omic_stabl_cv(\n\tX=X,\n\ty=y.astype(int),\n\touter_splitter=outer_splitter,\n\tstabl=stabl,\n\tstability_selection=stability_selection,\n\ttask_type='binary',\n\tsave_path='./Results',\n\touter_groups=None)\n")

def univariate_analysis(fpy):
    fpy.write("\n")
    fpy.write("#Univariate\n")
    fpy.write("os.makedirs('./Results/Univariate', exist_ok=True)\n")
    fpy.write("vals1 = []\n")
    fpy.write("vals2 = []\n")
    fpy.write("for col in X.columns:\n")
    fpy.write("\ta,b = mannwhitneyu(X.loc[y == 0,col].to_numpy(),X.loc[y == 1,col].to_numpy())\n")
    fpy.write("\tvals1.append(a)\n")
    fpy.write("\tvals2.append(b)\n")
    fpy.write("\n")
    fpy.write("res = pd.DataFrame(data=[vals1,vals2],index= ['Mann-Whitney U-test','p-value'],columns=X.columns)\n")
    fpy.write("res = res.sort_values(by='p-value',axis=1)\n")
    fpy.write("res.T.to_csv('./Results/Univariate/' + 'Mann-WhitneyU-testPval.csv')\n")
    fpy.write("\n")
    fpy.write("boxplot_features(\n\tlist_of_features=res.columns[:10],\n\tdf_X=X[res.columns[:10]],\n\ty=y,\n\tshow_fig=False,\n\texport_file=True,\n\tpath ='./Results/Univariate'\n)\n")

def final_stabl(fpy, preprocess):
    fpy.write("\n")
    fpy.write("#Final STABL\n")
    fpy.write("finalstabl = clone(stabl)\n")
    if preprocess:
        fpy.write("finalstabl.fit(X_STD,y.astype(int))\n")
        fpy.write("\n")
        fpy.write("save_stabl_results(finalstabl,'./Results'+'/FinalSTABL/',X_STD,y,task_type='binary')\n")
    else: 
        fpy.write("finalstabl.fit(X, y.astype(int))\n")
        fpy.write("\n")
        fpy.write("save_stabl_results(finalstabl,'./Results'+'/FinalSTABL/',X,y,task_type='binary')\n")

        
# outer_splitter = LeaveOneOut()

# def run(timePoint,stablIdx):


#     single_omic_stabl_cv(
#     X=data,
#     y=label.astype(int),
#     outer_splitter=outer_splitter,
#     stabl=stablList[stablIdx],
#     stability_selection=stability_selection,
#     task_type="binary",
#     save_path=Path(resultFolder),
#     )
#     stabl = clone(stablList[stablIdx])
#     stabl.fit(dataSTD,label.astype(int))


#     save_stabl_results(stabl,resultFolder+"/FinalSTABL/",dataSTD,label,task_type="binary")





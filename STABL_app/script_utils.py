
import os
from pathlib import Path
import re
from subwindows import show_message

def test_script(foldername, X_file, y_col = "", y_file = ""):
    if has_special_chars_or_spaces(foldername):
        show_message("Error", "Your STABL Run Name contains undesired characters or spaces, please chose another name.")
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
    else :
        os.makedirs(foldername)
        with open(Path(foldername, foldername + '.py'), 'w') as fpy:
            # TO DO write the python file to run STABL the way it is asked
            import_lib(fpy)
            import_data(fpy, X_file, y_col, y_file)
            fpy.close()
        with open(Path(foldername, foldername + '.sbatch'), 'w') as fsbatch:
            # TO DO write the sbatch file to run the python script
            fsbatch.write("Test")
            fsbatch.close()
        if y_col == "":
            show_message("Warning", "You have not specified the column of your datafile containing your outcomes :\n\n* If there is no column corresponding to your outcomes in this file continue\n\n* If there is a column corresponding to your outcomes in your datafile please specify it\n(you'll need to fill the text box 'Outcome column' and then delete the folder that has just been created with your python script and sbatch file and finally clic on create)\n\nMake sure there is no column with your outcome in the data file otherwise you won't get the expected results.")
        

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
    fpy.write("import numpy as np\n")
    fpy.write("import pandas as pd\n")
    fpy.write("from pathlib import Path\n")
    fpy.write("from sklearn.model_selection import GroupShuffleSplit, RepeatedStratifiedKFold, LeaveOneOut\n")
    fpy.write("from sklearn.base import clone\n")
    fpy.write("from stabl.stabl import Stabl, plot_stabl_path, plot_fdr_graph, save_stabl_results\n")
    fpy.write("from stabl.preprocessing import LowInfoFilter, remove_low_info_samples\n")
    fpy.write("\n")
    fpy.write("#STABL pipelines\n")
    fpy.write("from stabl.multi_omic_pipelines import multi_omic_stabl, multi_omic_stabl_cv\n")
    fpy.write("from stabl.single_omic_pipelines import single_omic_stabl, single_omic_stabl_cv\n")
    fpy.write("from stabl.pipelines_utils import compute_features_table\n")   
    fpy.write("\n") 
    
def import_data(fpy, X_file, y_col, y_file):
    fpy.write(f"X = pd.read_csv('./{X_file}',index_col=0)\n")




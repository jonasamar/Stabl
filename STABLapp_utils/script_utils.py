#------------------------------------------------------------------------------------------------------------------------------
#
# Function : write_scripts
#
# Description :
#       - args : all the different parameters of the Stabl Model, the type of pipeline and the sbatch file 
#       - effect : calls successively functions to write the python script and the sbatch file with the parameters chosen by user
#
#------------------------------------------------------------------------------------------------------------------------------

import os
from pathlib import Path

from STABLapp_utils.subwindows.MessageWindow import show_message

from STABLapp_utils.ScriptComponents.ImportLibraries import import_lib
from STABLapp_utils.ScriptComponents.ImportData import import_data
from STABLapp_utils.ScriptComponents.StablClass import stabl_class
from STABLapp_utils.ScriptComponents.Preprocessing import preprocessing
from STABLapp_utils.ScriptComponents.OuterSplitter import outer_splitter
from STABLapp_utils.ScriptComponents.Pipeline import pipeline
from STABLapp_utils.ScriptComponents.Univariate import univariate_analysis
from STABLapp_utils.ScriptComponents.FinalStabl import final_stabl
from STABLapp_utils.ScriptComponents.ParamVerification import file_info_correct
from STABLapp_utils.ScriptComponents.WriteSbatch import write_sbatch


def write_scripts(version, 
                  foldername, 
                  X_file, y_col, y_file, 
                  l1_ratio, 
                  artificial_type, 
                  sample_fraction, 
                  bootstrap_replace, 
                  random_state, 
                  preprocess, 
                  outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size, 
                  stabl_pipeline, 
                  task_type, 
                  outer_groups, 
                  X_test, y_test_col, y_test, 
                  days, hours, minutes, sec, nb_cpu, mem_cpu):
    
    correct = file_info_correct(version, 
                                foldername, 
                                X_file, y_col, y_file, 
                                artificial_type, 
                                outersplitter, 
                                stabl_pipeline, 
                                task_type, 
                                X_test, y_test_col, y_test, 
                                days, hours, minutes, sec)
    
    if correct:
        os.makedirs(foldername, exist_ok=True)
        with open(Path(foldername, foldername + '.py'), 'w') as fpy:
            # write the python file to run STABL
            import_lib(fpy)
            import_data(version, fpy, foldername, X_file, y_col, y_file, stabl_pipeline)
            stabl_class(fpy, l1_ratio, artificial_type, sample_fraction, bootstrap_replace, random_state)
            if preprocess:
                preprocessing(fpy, stabl_pipeline)
            if '_cv' in stabl_pipeline:
                outer_splitter(fpy, outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size)
            pipeline(version, fpy, foldername, stabl_pipeline, task_type, outer_groups, X_test, y_test_col, y_test)
            univariate_analysis(fpy, foldername, task_type, stabl_pipeline)
            final_stabl(fpy, foldername, preprocess, stabl_pipeline, task_type)
            fpy.close()
        with open(Path(foldername, foldername + '.sbatch'), 'w') as fsbatch:
            # TO DO write the sbatch file to run the python script
            write_sbatch(fsbatch,foldername, days, hours, minutes, sec, nb_cpu, mem_cpu)
            fsbatch.close()
        
        # Warnings in case some missing information could lead to a wrong model
        if version =='v1' and y_col == "" and len(X_test) > 0 and y_test_col == "":
            show_message("Warning", "You have not specified the column of your (VALIDATION nor TRAINING) datafile containing your outcomes :\n\n\t* If there is no column corresponding to your outcomes in this file continue\n\n\t* If there is a column corresponding to your outcomes in your datafile please specify it\n(you'll need to fill the text box 'Outcome column' and then delete the folder that has just been created with your python script and sbatch file and finally clic on create)\n\nMake sure there is no column with your outcome in the data file otherwise you won't get the expected results.")
        elif version == 'v1' and y_col == "":
            show_message("Warning", "You have not specified the column of your datafile containing your outcomes :\n\n\t* If there is no column corresponding to your outcomes in this file continue\n\n\t* If there is a column corresponding to your outcomes in your datafile please specify it\n(you'll need to fill the text box 'Outcome column' and then delete the folder that has just been created with your python script and sbatch file and finally clic on create)\n\nMake sure there is no column with your outcome in the data file otherwise you won't get the expected results.")
        elif version == 'v1' and len(X_test) > 0 and y_test_col == "":
            show_message("Warning", "You have not specified the column of your VALIDATION datafile containing your outcomes :\n\n\t* If there is no column corresponding to your outcomes in this file continue\n\n\t* If there is a column corresponding to your outcomes in your datafile please specify it\n(you'll need to fill the text box 'Outcome column' and then delete the folder that has just been created with your python script and sbatch file and finally clic on create)\n\nMake sure there is no column with your outcome in the data file otherwise you won't get the expected results.")
        else:
            show_message("info", f"{foldername} folder created and completed !\nYou can now run STABL on Sherlock !")




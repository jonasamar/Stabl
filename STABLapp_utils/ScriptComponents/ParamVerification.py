#------------------------------------------------------------------------------------------------------------------------------
#
# Function : file_info_correct
#
# Description :
#       - arguments : all the parameters selected by the user requiring verifications.
#       - effect : If there is a parameter with unwanted values, the function send an error message with the description of the
#                   error. Otherwise, the function return true so that the write_scripts function from scripts_utils.py can 
#                   create the python and sbatch files.
#
#------------------------------------------------------------------------------------------------------------------------------

import re

from STABLapp_utils.subwindows.MessageWindow import show_message

def file_info_correct(version, 
                      foldername, 
                      X_file, y_col, y_file, 
                      artificial_type, 
                      outersplitter, 
                      stabl_pipeline, 
                      task_type, 
                      X_test, y_test_col, y_test, 
                      days, hours, minutes, sec):
    if has_special_chars_or_spaces(foldername) or len(foldername) == 0:
        show_message("Error", "Your STABL Run Name contains undesired characters or spaces or is empty, please chose another name.")
        return False
    elif not artificial_type in ["random_permutation", "knockoff"]:
        show_message("Error", "The artificial type you selected is not recognized. Make sure it is either random_permutation or knockoff.")
        return False
    elif not outersplitter in ['LeaveOneOut', 'RepeatedStratifiedKFold', 'GroupShuffleSplit']:
        show_message("Error", "The outer splitter you have selected is not recognized. Please chose between:\n\t*LeaveOneOut\n\t*RepeatedStratifiedKFold\n\t*GroupShuffleSplit")
        return False
    elif not task_type in ['binary', 'regression']:
        show_message("Error", "The task_type you have selected is not recognized. Please chose between:\n\t*'binary'\n\t*'regression'")
        return False
    elif not (is_positive_integer(days) and is_positive_integer(hours) and is_positive_integer(minutes) and is_positive_integer(sec)) or len(sec) !=2 or len(minutes) !=2:
        show_message("Error", "Your time limit is not recognized.\nPlease make sure days, hours, minutes and sec are positive integer numbers\nand that minutes and seconds are two digits numbers.")
        return False
    elif version == 'v1': # verifications for v1
        if X_file[-4:] != ".csv":
            show_message("Error", "Your datafile name doesn't correspond to a csv file name. Please convert it to a csv file before creating your python script.")
            return False
        elif y_file[-4:] != ".csv":
            show_message("Error", "Your outcome file name doesn't correspond to a csv file name. Please convert it to a csv file before creating your python script.")
            return False
        elif len(X_file) < 5:
            show_message("Error", "Your datafile name is incorrect. It should be a csv file and the name should contain 5 characters or more.")
            return False
        elif len(y_file) < 5:
            show_message("Error", "Your outcome file name is incorrect. It should be a csv file and the name should contain 5 characters or more.")
            return False
        elif y_col == "" and y_file == "":
            show_message("Error", "You have not specified where to find the outcomes you want to predict. Please, specify the column of your dataset corresponding to the outcomes and/or specify the name of the csv file containing your outcomes.")
            return False
        elif stabl_pipeline in ["multi_omic_stabl",  "single_omic_stabl"] and len(X_test) > 0: #when X_test is put as input, we expect all the optional inputs otherwise X_test = None and y_test = None
            if X_test[-4:] != ".csv":
                show_message("Error", "Your validation features file name doesn't correspond to a csv file name. Please convert it to a csv file before creating your python script.")
                return False
            elif y_test[-4:] != ".csv":
                show_message("Error", "Your VALIDATION outcome file name doesn't correspond to a csv file name. Please convert it to a csv file before creating your python script.")
                return False
            elif len(X_test) < 5:
                show_message("Error", "Your validation features file name is incorrect. It should be a csv file and the name should contain 5 characters or more.")
                return False
            elif len(y_test) < 5:
                show_message("Error", "Your VALIDATION outcome file name is incorrect. It should be a csv file and the name should contain 5 characters or more.")
                return False
            elif y_test_col == "" and y_test == "":
                show_message("Error", "You have not specified where to find the VALIDATION outcomes you want to predict. Please, specify the column of your dataset corresponding to the outcomes and/or specify the name of the csv file containing your outcomes,\nin the validation features frame.")
                return False
    elif version == 'v2':
        if len(X_file) == 0:
            show_message("Error", "You are missing data files.\nPlease import a 'training features' file and try to create your script again.")
            return False
        elif len(y_file.split('\n'))-1 != 1:
            n = len(y_file.split('\n'))-1
            show_message("Error", f"You imported {n} training outcomes files instead of 1.\nPlease chose one training outcomes file and try creating your scripts again.")
            return False
        elif 'multi' in stabl_pipeline:
            files = X_file.split('\n')
            file_types = set()
            for file in files:
                if len(file) > 0:
                    elements = file.split('\t')
                    file_types.add(elements[1])
                    if elements[1] == ' ':
                        show_message("Error", f"You are running a multi omic pipeline and have not specified the nature\nof the data in {elements[0]} (CyTOF, Proteomics, ...).\nPlease specify the data contained in this file and try creating your script again.")
                        return False
            if (not '_cv' in stabl_pipeline) and len(X_test) > 0:
                test_files = X_test.split('\n')
                test_file_types = set()
                for file in test_files:
                    if len(file) > 0:
                        elements = file.split('\t')
                        test_file_types.add(elements[1])
                        if elements[1] == ' ':
                            show_message("Error", f"You are running a multi omic pipeline and have not specified the nature\nof the data in {elements[0]} (CyTOF, Proteomics, ...).\nPlease specify the data contained in this file and try creating your script again.")
                            return False
                if test_file_types != file_types:
                    show_message("Error", f"Nature of the files in your training features files : {file_types}.\nNature of the files in your validation features files : {test_file_types}.\nYou must have the same nature of data in your training and validation features file.\nPlease change your files and try to create your scripts again.")
                    return False
                elif len(files) != len(test_files):
                    show_message("Error", f"You should have the same number of training features files and validation features files.\nYou currently have {len(files)-1} training features files and {len(test_files)-1} validation features files.\nPlease change your files and try creating your scripts again.")
                    return False
            if not '_cv' in stabl_pipeline:
                if (len(y_test) > 0) and (len(X_test)==0):
                    show_message("Error", "You have imported a validation outcomes file and omitted validation features file.")
                    return False
                elif (len(X_test) > 0) and (len(y_test.split('\n'))-1 != 1):
                    n = len(y_test.split('\n'))-1
                    show_message("Error", f"You have imported a validation features file and imported {n} validation ouctomes file instead of one.")
                    return False
                elif ('single' in stabl_pipeline) and (len(y_test) > 0) and (len(X_test.split('\n'))-1 != 1):
                    n = len(X_test.split('\n'))-1
                    show_message("Error", f"You have chosen a single omic pipeline and imported {n} validation features files instead of 1.\nPlease chose one validation features file and try creating your scripts again.")
                    return False
            if '_cv' in stabl_pipeline:
                if len(X_test) > 0:
                    show_message("Error", "You have selected a cross validation pipeline and yet you imported validation features...\nChose the right pipeline or remove useless data and try creating your scripts again.")
                    return False
                elif len(y_test) > 0:
                    show_message("Error", "You have selected a cross validation pipeline and yet you imported validation ouctomes...\nChose the right pipeline or remove useless data and try creating your scripts again.")
                    return False
        elif 'single' in stabl_pipeline :
            if len(X_file.split('\n'))-1 !=1:
                n = len(X_file.split('\n'))-1
                show_message("Error", f"You have chosen a single omic pipeline and imported {n} training features files instead of 1.\nPlease chose one training features file and try creating your scripts again.")
                return False
            elif not '_cv' in stabl_pipeline:
                if (len(y_test) > 0) and (len(X_test)==0):
                    show_message("Error", "You have imported a validation outcomes file and omitted validation features file.")
                    return False
                elif (len(X_test) > 0) and (len(y_test.split('\n'))-1 != 1):
                    n = len(y_test.split('\n'))-1
                    show_message("Error", f"You have imported a validation features file and imported {n} validation ouctomes file instead of one.")
                    return False
                elif ('single' in stabl_pipeline) and (len(y_test) > 0) and (len(X_test.split('\n'))-1 != 1):
                    n = len(X_test.split('\n'))-1
                    show_message("Error", f"You have chosen a single omic pipeline and imported {n} validation features files instead of 1.\nPlease chose one validation features file and try creating your scripts again.")
                    return False
            elif '_cv' in stabl_pipeline:
                if len(X_test) > 0:
                    show_message("Error", "You have selected a cross validation pipeline and yet you imported validation features...\nChose the right pipeline or remove useless data and try creating your scripts again.")
                    return False
                elif len(y_test) > 0:
                    show_message("Error", "You have selected a cross validation pipeline and yet you imported validation ouctomes...\nChose the right pipeline or remove useless data and try creating your scripts again.")
                    return False
    return True

def has_special_chars_or_spaces(input_string):
    pattern = re.compile('[^A-Za-z0-9]+') 
    return bool(pattern.search(input_string))

def is_positive_integer(s):
    if not s.isdigit():
        return False
    n = int(s)
    return n >= 0
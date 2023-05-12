import re
from subwindows import show_message

def has_special_chars_or_spaces(input_string):
    pattern = re.compile('[^A-Za-z0-9]+') 
    return bool(pattern.search(input_string))

def is_positive_integer(s):
    if not s.isdigit():
        return False
    n = int(s)
    return n >= 0

def file_info_correct(foldername, X_file, y_col, y_file, artificial_type, outersplitter, stabl_pipeline, task_type, X_test, y_test_col, y_test, days, hours, minutes, sec):
    if has_special_chars_or_spaces(foldername) or len(foldername) == 0:
        show_message("Error", "Your STABL Run Name contains undesired characters or spaces or is empty, please chose another name.")
        return False
    elif not artificial_type in ["random_permutation", "knockoff"]:
        show_message("Error", "The artificial type you selected is not recognized. Make sure it is either random_permutation or knockoff.")
        return False
    elif not outersplitter in ['LeaveOneOut', 'RepeatedStratifiedKFold', 'GroupShuffleSplit']:
        show_message("Error", "The outer splitter you have selected is not recognized. Please chose between:\n\t*LeaveOneOut\n\t*RepeatedStratifiedKFold\n\t*GroupShuffleSplit")
        return False
    elif X_file[-4:] != ".csv":
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
    elif not task_type in ['binary', 'regression']:
        show_message("Error", "The task_type you have selected is not recognized. Please chose between:\n\t*'binary'\n\t*'regression'")
        return False
    elif stabl_pipeline in ["multi_omic_stabl",  "single_omic_stabl"] and len(X_test) > 0: #when X_test is put as input, we expect all the optional inputs otherwise X_test = None and y_test = None
        if X_test[-4:] != ".csv":
            show_message("Error", "Your VALIDATION datafile name doesn't correspond to a csv file name. Please convert it to a csv file before creating your python script.")
            return False
        elif y_test[-4:] != ".csv":
            show_message("Error", "Your VALIDATION outcome file name doesn't correspond to a csv file name. Please convert it to a csv file before creating your python script.")
            return False
        elif len(X_test) < 5:
            show_message("Error", "Your VALIDATION datafile name is incorrect. It should be a csv file and the name should contain 5 characters or more.")
            return False
        elif len(y_test) < 5:
            show_message("Error", "Your VALIDATION outcome file name is incorrect. It should be a csv file and the name should contain 5 characters or more.")
            return False
        elif y_test_col == "" and y_test == "":
            show_message("Error", "You have not specified where to find the VALIDATION outcomes you want to predict. Please, specify the column of your dataset corresponding to the outcomes and/or specify the name of the csv file containing your outcomes,\nin the VALIDATION Data frame.")
            return False
    elif not (is_positive_integer(days) and is_positive_integer(hours) and is_positive_integer(minutes) and is_positive_integer(sec)) or len(sec) !=2 or len(minutes) !=2:
        show_message("Error", "Your time limit is not recognized.\nPlease make sure days, hours, minutes and sec are positive integer numbers\nand that minutes and seconds are two digits numbers.")
        return False
    return True
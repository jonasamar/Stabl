
import os
from pathlib import Path

from subwindows import show_message
from ScriptComponents.importLibraries import import_lib
from ScriptComponents.importData import import_data
from ScriptComponents.stablClass import stabl_class
from ScriptComponents.preprocessing import preprocessing
from ScriptComponents.outersplitter import outer_splitter
from ScriptComponents.pipeline import pipeline
from ScriptComponents.univariate import univariate_analysis
from ScriptComponents.finalStabl import final_stabl
from ScriptComponents.infoverification import file_info_correct
from ScriptComponents.writesbatch import write_sbatch


def write_scripts(foldername, X_file, y_col, y_file, l1_ratio, artificial_type, sample_fraction, replace, random_state, preprocess, outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size, stabl_pipeline, task_type, outer_groups, X_test, y_test_col, y_test):
    correct = file_info_correct(foldername, X_file, y_col, y_file, artificial_type, outersplitter, stabl_pipeline, task_type, X_test, y_test_col, y_test)
    if correct:
        os.makedirs(foldername)
        with open(Path(foldername, foldername + '.py'), 'w') as fpy:
            # write the python file to run STABL
            import_lib(fpy)
            import_data(fpy, X_file, y_col, y_file)
            stabl_class(fpy, l1_ratio, artificial_type, sample_fraction, replace, random_state)
            if preprocess:
                preprocessing(fpy)
            outer_splitter(fpy, outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size)
            pipeline(fpy, stabl_pipeline, task_type, outer_groups, X_test, y_test_col, y_test)
            univariate_analysis(fpy, task_type)
            final_stabl(fpy, preprocess)
            fpy.close()
        with open(Path(foldername, foldername + '.sbatch'), 'w') as fsbatch:
            # TO DO write the sbatch file to run the python script
            write_sbatch(fsbatch,foldername)
            fsbatch.close()
        if y_col == "" and len(X_test) > 0 and y_test_col == "":
            show_message("Warning", "You have not specified the column of your (VALIDATION nor TRAINING) datafile containing your outcomes :\n\n\t* If there is no column corresponding to your outcomes in this file continue\n\n\t* If there is a column corresponding to your outcomes in your datafile please specify it\n(you'll need to fill the text box 'Outcome column' and then delete the folder that has just been created with your python script and sbatch file and finally clic on create)\n\nMake sure there is no column with your outcome in the data file otherwise you won't get the expected results.")
        elif y_col == "":
            show_message("Warning", "You have not specified the column of your datafile containing your outcomes :\n\n\t* If there is no column corresponding to your outcomes in this file continue\n\n\t* If there is a column corresponding to your outcomes in your datafile please specify it\n(you'll need to fill the text box 'Outcome column' and then delete the folder that has just been created with your python script and sbatch file and finally clic on create)\n\nMake sure there is no column with your outcome in the data file otherwise you won't get the expected results.")
        elif len(X_test) > 0 and y_test_col == "":
            show_message("Warning", "You have not specified the column of your VALIDATION datafile containing your outcomes :\n\n\t* If there is no column corresponding to your outcomes in this file continue\n\n\t* If there is a column corresponding to your outcomes in your datafile please specify it\n(you'll need to fill the text box 'Outcome column' and then delete the folder that has just been created with your python script and sbatch file and finally clic on create)\n\nMake sure there is no column with your outcome in the data file otherwise you won't get the expected results.")




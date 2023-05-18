#------------------------------------------------------------------------------------------------------------------------------
#
# Function : show_settings_and_create_files
#
# Description :
#       - arguments : Stabl, pipeline and sbatch file settings chosen by the user.
#       - effect : Open a new window with a recap of all the settings chosen by the user so that he or she can check the
#                   parameters one last time before creating the python and sbatch files.
#                   This function is also useful because it allows the reorganization of the variable file_list.
#                   We separate the different files into the variables X_file, y_file, X_test, y_test, outer_groups so that we
#                   can use the write_scripts function from the v1 version of the app.
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter

import re

from STABLapp_utils.SubframeComponents.ConfirmationWindow.RecapFiles import recap_files_and_var_reorganization
from STABLapp_utils.SubframeComponents.ConfirmationWindow.RecapPipeline import recap_pipeline_params
from STABLapp_utils.SubframeComponents.ConfirmationWindow.RecapStabl import recap_stabl_params
from STABLapp_utils.SubframeComponents.ConfirmationWindow.RecapSbatch import recap_sbatch_params

from STABLapp_utils.subwindows.MessageWindow import show_message

from STABLapp_utils.script_utils import write_scripts

def show_settings_and_create_files(foldername, 
                                   l1_ratio, 
                                   artificial_type, 
                                   sample_fraction, 
                                   bootstrap_replace, 
                                   random_state, 
                                   preprocess, 
                                   outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size, 
                                   pipeline, 
                                   task_type, 
                                   days, hours, minutes, sec, nb_cpu, mem_cpu, 
                                   file_list,
                                   X_file, y_col, y_file,
                                   X_test, y_test_col, y_test,
                                   outer_groups):
    
    if has_special_chars_or_spaces(foldername.get()) or len(foldername.get()) == 0:
        show_message("Error", "Your STABL Run Name contains undesired characters or spaces or is empty, please chose another name.")
    else:
        # Window
        window = customtkinter.CTk()
        window.geometry("800x700")
        window.title('Confirmation window')
        
        title = customtkinter.CTkLabel(window, justify='center', text=foldername.get())
        title.pack(padx=10, pady=6)
        
        SubframeInfo = customtkinter.CTkFrame(window)
        SubframeInfo.pack(side='top', fill='both', padx=10, pady=6)
        info = customtkinter.CTkLabel(SubframeInfo, justify='center', text='Below are the values of the parameters you are going to run STABL with.\nPlease verify they are correct and then click on Create Scripts.')
        info.pack(padx=10, pady=6)
        
        leftpanel = customtkinter.CTkFrame(window, width=200, height=100)
        leftpanel.pack(side="left", fill='both', padx=(10, 5), pady=10, expand=True)
        rightpanel = customtkinter.CTkFrame(window, width=200, height=100)
        rightpanel.pack(side="left", fill='both', padx=(5, 10), pady=10, expand=True)
        
        recap_files_and_var_reorganization(leftpanel, file_list, X_file, y_file, X_test, y_test, outer_groups)
        recap_pipeline_params(leftpanel, preprocess, outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size, pipeline, task_type)
        recap_stabl_params(rightpanel, l1_ratio, artificial_type, sample_fraction, bootstrap_replace, random_state)
        recap_sbatch_params(rightpanel, days, hours, minutes, sec, nb_cpu, mem_cpu)

        SubframeButtons = customtkinter.CTkFrame(rightpanel)
        SubframeButtons.pack(side='top', fill='both', padx=10, pady=6, expand=True)
        close_button = customtkinter.CTkButton(SubframeButtons, text="Close", command=window.destroy)
        close_button.pack(side='left', padx=10, pady=6)
        CreationButton = customtkinter.CTkButton(master=SubframeButtons, 
                                                text="Create Script", 
                                                command= lambda : write_scripts('v2', 
                                                                                foldername.get(), 
                                                                                X_file.get(), y_col.get(), y_file.get(), 
                                                                                l1_ratio.get(), 
                                                                                artificial_type.get(), 
                                                                                sample_fraction.get(), 
                                                                                bootstrap_replace.get(), 
                                                                                random_state.get(), 
                                                                                preprocess.get(), 
                                                                                outersplitter.get(), n_splits.get(), n_repeat.get(), cv_rd.get(), test_size.get(), train_size.get(), 
                                                                                pipeline.get(), 
                                                                                task_type.get(), 
                                                                                outer_groups.get(), 
                                                                                X_test.get(), y_test_col.get(), y_test.get(), 
                                                                                days.get(), hours.get(), minutes.get(), sec.get(), nb_cpu.get(), mem_cpu.get()))
        CreationButton.pack(side="right", pady=12, padx=10)
        
        window.mainloop()

def has_special_chars_or_spaces(input_string):
    pattern = re.compile('[^A-Za-z0-9]+') 
    return bool(pattern.search(input_string))
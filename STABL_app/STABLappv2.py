#------------------------------------------------------------------------------------------------------------------------------
#
# Function : app_v2
#
# Description :
#       This a second attempt at creating a STABL interface. In this version, single and multi omic pipelines were taken into account.
#       In order to run STABL on Sherlock, a user would need to use this interface to create a new folder containing the
#       generated python script and sbatch file.
#       In this version, the user can directly import his or her files thanks to the interface.
#       The interface is also built to help the user understand the role of the parameters he or she is using with a click 
#       interaction on the name of the parameters with a star (*).
#       Some finer tunable parameters are left for next versions.
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter

from Subframes.subframeFoldername import subframeFoldername_display
from Subframes.subframeFiles import subframeFiles_display
from Subframes.subframeStabl import subframeStabl_display
from Subframes.subframePipeline import subframePipeline_display
from Subframes.subframeSbatch import subframeSbatch_display

from subwindows.ConfirmationWindow import show_settings_and_create_files

def app_v2():
    # Master
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()
    root.geometry("1350x800")
    root.title("STABL interface")
    
    # Variables
    foldername = customtkinter.StringVar()
    file_list = customtkinter.StringVar() # New variable : to contain many file names and descriptions
    
    l1_ratio = customtkinter.DoubleVar(value='1.')
    artificial_type = customtkinter.StringVar(value='random_permutation')
    sample_fraction = customtkinter.DoubleVar(value='0.5')
    bootstrap_replace = customtkinter.BooleanVar(value=False)
    random_state = customtkinter.IntVar(value=42)
    
    preprocess = customtkinter.BooleanVar(value=True)
    
    outersplitter = customtkinter.StringVar(value='RepeatedStratifiedKFold')
    n_splits = customtkinter.IntVar(value=5)
    n_repeat = customtkinter.IntVar(value=10)
    cv_rd = customtkinter.IntVar(value=42)
    test_size = customtkinter.DoubleVar(value=0.2)
    train_size = customtkinter.DoubleVar(value=None)
    
    pipeline = customtkinter.StringVar(value='single_omic_stabl_cv')
    task_type = customtkinter.StringVar(value='binary')
    
    days = customtkinter.StringVar(value="2")
    hours = customtkinter.StringVar(value="00")
    minutes = customtkinter.StringVar(value="00")
    sec = customtkinter.StringVar(value="00")
    nb_cpu = customtkinter.StringVar(value="2")
    mem_cpu = customtkinter.StringVar(value="16 GB")
    
    # Variables (used to reorganize file_list)
    X_file = customtkinter.StringVar()
    y_col = customtkinter.StringVar()
    y_file = customtkinter.StringVar()
    outer_groups = customtkinter.StringVar(value=None)
    X_test = customtkinter.StringVar(value=None)
    y_test_col = customtkinter.StringVar(value=None)
    y_test = customtkinter.StringVar(value=None)

    # Window
    label = customtkinter.CTkLabel(master=root, text="Creation of python & sbatch scripts", font=("Roboto", 20)) 
    label.pack(pady=6, padx=10)
    
    leftpanel = customtkinter.CTkFrame(root, width=200, height=100, border_color="black")
    leftpanel.pack(side="left", fill='both', padx=(10, 5), pady=10)
    rightpanel = customtkinter.CTkFrame(root, width=200, height=100, border_color="black")
    rightpanel.pack(side="left", fill='both', padx=(5, 10), pady=10)
    
    # Subframes
    
    ## left panel
    
    subframeFoldername_display(leftpanel, foldername, file_list)
    
    label1 = customtkinter.CTkLabel(leftpanel, text="Python File Settings", font=("Roboto", 16, "bold")) 
    label1.pack(padx=15, pady=15)
    
    subframeFiles_display(leftpanel, foldername, file_list)
    
    subframePipeline_display('v2', 
                             leftpanel,
                             preprocess, 
                             outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size, 
                             pipeline, 
                             task_type)
    
    ## right panel
    subframeStabl_display(rightpanel, l1_ratio, artificial_type, sample_fraction, bootstrap_replace, random_state)
    
    subframeSbatch_display(rightpanel, days, hours, minutes, sec, nb_cpu, mem_cpu)
    
    CreationButton = customtkinter.CTkButton(master=rightpanel, 
                                             text="Create", 
                                             command= lambda : show_settings_and_create_files(foldername, 
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
                                                                                                outer_groups))
    CreationButton.pack(side="top", pady=12, padx=10)

    root.mainloop()

app_v2()

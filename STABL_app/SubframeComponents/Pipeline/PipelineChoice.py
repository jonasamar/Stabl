#------------------------------------------------------------------------------------------------------------------------------
#
# Function : pipeline_choice
#
# Description :
#       - arguments : version, subframe, parameters linked to the choice of pipeline
#       - effect : Display
#                   - a combobox to chose the stabl pipeline
#                   - (v1) a textbox to enter the outergroups parameter when the pipeline is a cross validation pipeline
#                   - (v1) 3 textboxes to enter X_test, y_test (and even y_col_test) when it is a validation pipeline
#                   - a combobox to chose the outersplitter
#                   - a button to open a new window in which the user can tune the parameters of the outer splitter
#                   - a combobox to chose the outersplitter when the pipeline is a cross validation pipeline
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter

from subwindows.MessageWindow import show_message

from SubframeComponents.Pipeline.OuterSplitterParams import outersplitter_params_tuning

def pipeline_choice(version, 
                    subframe, 
                    pipeline, 
                    outer_groups, 
                    X_test, y_test_col, y_test, 
                    outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size):
    
    if version == 'v1':
        available_pipelines = ["single_omic_stabl", "single_omic_stabl_cv"]
    elif version == 'v2':
        available_pipelines = ["multi_omic_stabl", "multi_omic_stabl_cv", "single_omic_stabl", "single_omic_stabl_cv"]

    appear = True
    
    #outer_groups
    subframegroups = customtkinter.CTkFrame(subframe, width=200, height=100)
    labelgroups = customtkinter.CTkLabel(subframegroups, text="Outer groups *")
    outergroups = customtkinter.CTkEntry(subframegroups, textvariable = outer_groups, justify='center')
    
    #X_test and y_test
    labeltest = customtkinter.CTkLabel(subframe, text="Validation dataset *")
    
    subframeX = customtkinter.CTkFrame(subframe, width=200, height=100)
    subframeColY = customtkinter.CTkFrame(subframe, width=200, height=100)
    subframeY = customtkinter.CTkFrame(subframe, width=200, height=100)

    labelX = customtkinter.CTkLabel(subframeX, text="Datafile Name *")
    datafileX = customtkinter.CTkEntry(master=subframeX, textvariable = X_test, justify='center', placeholder_text="None")

    labelColY = customtkinter.CTkLabel(subframeColY, text="Outcome column *")
    ColY = customtkinter.CTkEntry(master=subframeColY, textvariable=y_test_col, justify='center', placeholder_text="None")

    labelY = customtkinter.CTkLabel(subframeY, text="Outcome file *")
    datafileY = customtkinter.CTkEntry(master=subframeY, textvariable=y_test, justify='center', placeholder_text="None")
    
    # Outer splitter
    subframeSplit = customtkinter.CTkFrame(subframe, width=200, height=100)
    
    labelsplit = customtkinter.CTkLabel(subframeSplit, text="Outer splitter *")
   
    comboboxsplit = customtkinter.CTkComboBox(subframeSplit, variable=outersplitter, values=["GroupShuffleSplit", "RepeatedStratifiedKFold", "LeaveOneOut"], width=300)
    
    ParamButton = customtkinter.CTkButton(master=subframeSplit, text="Parameters", command= lambda : outersplitter_params_tuning(outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size))
    
    #else
    labelelse = customtkinter.CTkLabel(subframe, text="The pipeline selected is not recognized...\nChose one of the pipelines that are suggested above.")
    
    # Function that activate the frame containing the parameters from the validation pipelines
    def val_params(appear):
        if appear and version == 'v1':
            labeltest.pack()
            labeltest.bind("<Button-1>", lambda event : show_message("info", "Indicate the name of the data files containing data independent from the training data indicated earlier.\nThis data will be used to validate the performances of your model."))
            subframeX.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
            subframeColY.pack(side="left", fill="both", expand=True, padx=5, pady=10)
            subframeY.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)
            labelX.pack()
            labelX.bind("<Button-1>", lambda event : show_message("info", "The name you enter should correspond to the file with your entire validation/test dataset."))
            datafileX.pack(pady=6, padx=10)
            labelColY.pack()
            labelColY.bind("<Button-1>", lambda event : show_message("info","If the file containing your entire validation/test dataset also contains the outcome you want to predict, you have to specify the name of the column corresponding to your outcome. Otherwise, leave this text box blank."))
            ColY.pack(pady=6, padx=10)
            labelY.pack()
            labelY.bind("<Button-1>", lambda event : show_message("info","If you have a distinct file with the outcome of your validation/test dataset, enter the name of the file in this text box. Otherwise, leave this text box blank."))
            datafileY.pack(pady=6, padx=10)
        else:
            labeltest.pack_forget()
            subframeX.pack_forget()
            subframeColY.pack_forget()
            subframeY.pack_forget()
            labelX.pack_forget()
            datafileX.pack_forget
            labelColY.pack_forget()
            ColY.pack_forget
            labelY.pack_forget()
            datafileY.pack_forget()
    
    # Function that activate the frame containing the parameters from the cross validation pipelines
    def cv_params(appear):
        if appear and version == 'v1':
            subframeSplit.pack(side="top", fill="both", padx=10, pady=6)
            labelsplit.pack(side="left", fill="both", padx=(20, 10))
            labelsplit.bind("<Button-1>", lambda event : show_message("info","Method used to separate the training set during the cross validation. You can chose between:\n\nGroupShuffleSplit : Provides randomized train/test indices to split data according to a third-party provided group.\n\t\tThis group information can be used to encode arbitrary domain specific stratifications of the\n\t\tsamples as integers. For instance the groups could be the year of collection of the samples and thus allow\n\t\tfor cross-validation against time-based splits.\n\nRepeatedStratifiedKFold : Repeats Stratified K-Fold n times with different randomization in each repetition.\n\nLeaveOneOut : Provides train/test indices to split data in train/test sets. Each sample is used\n\t\tonce as a test set (singleton) while the remaining samples form the training set."))
            comboboxsplit.pack(side="left", fill="both", padx=10, pady=5)
            ParamButton.pack(side="left", padx=(5,10))
            subframegroups.pack(side="top", fill="both", padx=10, pady=6)
            labelgroups.pack(side="left", fill="both", padx=(10, 5))
            labelgroups.bind("<Button-1>", lambda event : show_message("info","Enter the name of the csv file containing the groups."))
            outergroups.pack(side="left", fill="both", padx=10, pady=5)
            
        elif appear and version == 'v2':
            subframeSplit.pack(side="top", fill="both", padx=10, pady=6)
            labelsplit.pack(side="left", fill="both", padx=(20, 10))
            labelsplit.bind("<Button-1>", lambda event : show_message("info","Method used to separate the training set during the cross validation. You can chose between:\n\nGroupShuffleSplit : Provides randomized train/test indices to split data according to a third-party provided group.\n\t\tThis group information can be used to encode arbitrary domain specific stratifications of the\n\t\tsamples as integers. For instance the groups could be the year of collection of the samples and thus allow\n\t\tfor cross-validation against time-based splits.\n\nRepeatedStratifiedKFold : Repeats Stratified K-Fold n times with different randomization in each repetition.\n\nLeaveOneOut : Provides train/test indices to split data in train/test sets. Each sample is used\n\t\tonce as a test set (singleton) while the remaining samples form the training set."))
            comboboxsplit.pack(side="left", fill="both", padx=10, pady=5)
            ParamButton.pack(side="left", padx=(5,10))
            
        else:
            subframeSplit.pack_forget()
            labelsplit.pack_forget()
            comboboxsplit.pack_forget()
            ParamButton.pack_forget()
            subframegroups.pack_forget()
            labelgroups.pack_forget()
            outergroups.pack_forget()
            
    # Switch between the parameters of the cross validation pipelines and the ones of the validation pipelines
    def show_specific_params(event):
        if pipeline.get() in ["multi_omic_stabl_cv",  "single_omic_stabl_cv"]:
            cv_params(True)
            val_params(False)
            labelelse.pack_forget()
        elif pipeline.get() in ["multi_omic_stabl",  "single_omic_stabl"]:
            cv_params(False)
            val_params(True)
            labelelse.pack_forget()
        else:
            labelelse.pack()
            
    #choice of pipeline
    subframePip = customtkinter.CTkFrame(subframe, width=200, height=100)
    subframePip.pack(side="top", fill="both", padx=10, pady=6)
    
    labelpip = customtkinter.CTkLabel(subframePip, text="Pipeline *")
    labelpip.pack(side="left", fill="both", padx=(10, 5))
    labelpip.bind("<Button-1>", lambda event : show_message("info","You can chose a multi or single omic pipeline depending on the data you have.\nIn the name of some pipelines, you have 'cv' which stands for 'cross validation'"))
                   
    comboboxpip = customtkinter.CTkComboBox(subframePip, variable=pipeline, values=available_pipelines, width=250, command=show_specific_params)
    comboboxpip.pack(side="left", fill="both", padx=10, pady=5)
        
    cv_params(appear) #by default the pipeline is single_omic_stab_cv


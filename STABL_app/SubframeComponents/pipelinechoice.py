import customtkinter
from subwindows import show_message

def pipeline_choice(root, subframe, pipeline, task_type, outer_groups, X_test, y_test_col, y_test):
    subframeparams = customtkinter.CTkFrame(root, width=200, height=100)

    #outer_groups
    labelgroup = customtkinter.CTkLabel(subframeparams, text="Optional Parameter")

    subframegroups = customtkinter.CTkFrame(subframeparams, width=200, height=100)
    labelgroups = customtkinter.CTkLabel(subframegroups, text="Outer groups *")
    outergroups = customtkinter.CTkEntry(master=subframegroups, textvariable = outer_groups, justify='center')
    
    #X_test and y_test
    labeltest = customtkinter.CTkLabel(subframeparams, text="Validation dataset *")
    
    subframeX = customtkinter.CTkFrame(subframeparams, width=200, height=100)
    subframeColY = customtkinter.CTkFrame(subframeparams, width=200, height=100)
    subframeY = customtkinter.CTkFrame(subframeparams, width=200, height=100)

    labelX = customtkinter.CTkLabel(subframeX, text="Datafile Name *")
    datafileX = customtkinter.CTkEntry(master=subframeX, textvariable = X_test, justify='center', placeholder_text="None")

    labelColY = customtkinter.CTkLabel(subframeColY, text="Outcome column *")
    ColY = customtkinter.CTkEntry(master=subframeColY, textvariable=y_test_col, justify='center', placeholder_text="None")

    labelY = customtkinter.CTkLabel(subframeY, text="Outcome file *")
    datafileY = customtkinter.CTkEntry(master=subframeY, textvariable=y_test, justify='center', placeholder_text="None")
    
    #else
    labelelse = customtkinter.CTkLabel(subframeparams, text="The pipeline selected is not recognized...\nChose one of the pipelines that are suggested above.")
    
    # Function that activate the frame containing the parameters from the validation pipelines
    def val_params(appear):
        if appear:
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
        if appear:
            labelgroup.pack()
            subframegroups.pack(side="top", fill="both", padx=10, pady=6)
            labelgroups.pack(side="left", fill="both", padx=(10, 5))
            labelgroups.bind("<Button-1>", lambda event : show_message("info","Enter the name of the csv file containing the groups."))
            outergroups.pack(side="left", fill="both", padx=10, pady=5)
        else:
            labelgroup.pack_forget()
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
    subframePip.pack(side="left", fill="both", padx=(10,5), pady=5)
    
    labelpip = customtkinter.CTkLabel(subframePip, text="Pipeline *")
    labelpip.pack(side="left", fill="both", padx=(10, 5))
    labelpip.bind("<Button-1>", lambda event : show_message("info","You can chose a multi or single omic pipeline depending on the data you have.\nIn the name of some pipelines, you have 'cv' which stands for 'cross validation'"))
                   
    comboboxpip = customtkinter.CTkComboBox(subframePip, variable=pipeline, values=["multi_omic_stabl", "multi_omic_stabl_cv", "single_omic_stabl", "single_omic_stabl_cv"], width=250, command=show_specific_params)
    comboboxpip.pack(side="left", fill="both", padx=10, pady=5)
    
    #task_type
    subframettype = customtkinter.CTkFrame(subframe, width=200, height=100)
    subframettype.pack(side="left", fill="both", padx=(5,10), pady=5)
    
    labelttype = customtkinter.CTkLabel(subframettype, text="Task type *")
    labelttype.pack(side="left", fill="both", padx=(10, 5))
    labelttype.bind("<Button-1>", lambda event : show_message("info","binary : you have a classification problem and you want to predict 0 or 1 for a given sample.\n\nregression : you want to predict a value that takes a continous range of values (between  0 and 1 for instance)."))
                   
    comboboxttype = customtkinter.CTkComboBox(subframettype, variable=task_type, values=["binary", "regression"], width=150)
    comboboxttype.pack(side="left", fill="both", padx=10, pady=5)

    subframeparams.pack(side="top", fill="both", padx=10, pady=6)
    cv_params(True) #by default the pipeline is single_omic_stab_cv
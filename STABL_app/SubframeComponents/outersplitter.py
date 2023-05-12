import customtkinter
from subwindows import show_message

def outer_splitter_tuning(subframePipeline, outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size):
    subframeSplit = customtkinter.CTkFrame(subframePipeline, width=200, height=100)
    subframeSplit.pack(side="top", fill="both", padx=10, pady=6)

    labelsplit = customtkinter.CTkLabel(subframeSplit, text="Outer splitter *")
    labelsplit.pack(side="left", fill="both", padx=(20, 10))
    labelsplit.bind("<Button-1>", lambda event : show_message("info","Method used to separate the training set during the cross validation. You can chose between:\n\nGroupShuffleSplit : Provides randomized train/test indices to split data according to a third-party provided group.\n\t\tThis group information can be used to encode arbitrary domain specific stratifications of the\n\t\tsamples as integers. For instance the groups could be the year of collection of the samples and thus allow\n\t\tfor cross-validation against time-based splits.\n\nRepeatedStratifiedKFold : Repeats Stratified K-Fold n times with different randomization in each repetition.\n\nLeaveOneOut : Provides train/test indices to split data in train/test sets. Each sample is used\n\t\tonce as a test set (singleton) while the remaining samples form the training set."))

    comboboxsplit = customtkinter.CTkComboBox(subframeSplit, variable=outersplitter, values=["GroupShuffleSplit", "RepeatedStratifiedKFold", "LeaveOneOut"], width=300)
    comboboxsplit.pack(side="left", fill="both", padx=10, pady=5)
    
    ParamButton = customtkinter.CTkButton(master=subframeSplit, text="Parameters", command= lambda : tuning_outersplitter_param(outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size))
    ParamButton.pack(side="left", padx=(5,10))


def tuning_outersplitter_param(outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size):
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("dark-blue")
    
    paramwindow = customtkinter.CTk()
    paramwindow.geometry("400x400")
    paramwindow.title(outersplitter.get() + ' parameters')
    
    intro = customtkinter.CTkLabel(paramwindow, text=f"Here are the parameters of {outersplitter.get()}.\nYou can either keep them or change them.\nDon't forget to SAVE if you've changed parameters.")
    intro.pack(padx=10, pady=10)
    
    subframe = customtkinter.CTkFrame(paramwindow, width=200, height=100)
    subframe.pack(side="top", fill="both", padx=10, pady=6)
    
    if outersplitter.get() == 'LeaveOneOut':
        oneout = customtkinter.CTkLabel(subframe, text="No paramters")
        oneout.pack(padx=10, pady=6)
        close_button = customtkinter.CTkButton(paramwindow, text="Close", command=paramwindow.destroy)
        close_button.pack(padx=20, pady=20)
        
    elif outersplitter.get() == 'RepeatedStratifiedKFold':
        #n_splits
        subframeNsplit = customtkinter.CTkFrame(subframe, width=200, height=100)
        subframeNsplit.pack(side="top", fill="both", padx=10, pady=6)

        labelnsplit = customtkinter.CTkLabel(subframeNsplit, text="n_splits *")
        labelnsplit.pack(side="left", fill="both", padx=(10, 5))
        labelnsplit.bind("<Button-1>", lambda event : show_message("info","Number of folds in the cross validation. Must be at least 2.\nIt has to be an integer."))        
        Nsplitentry = customtkinter.CTkEntry(master=subframeNsplit, justify='center', placeholder_text=n_splits.get())
        Nsplitentry.pack(pady=6, padx=10, side='right')
        
        #n_repeat
        subframeRepeat = customtkinter.CTkFrame(subframe, width=200, height=100)
        subframeRepeat.pack(side="top", fill="both", padx=10, pady=6)

        labelnrep = customtkinter.CTkLabel(subframeRepeat, text="n_repeat *")
        labelnrep.pack(side="left", fill="both", padx=(10, 5))
        labelnrep.bind("<Button-1>", lambda event : show_message("info","Number of times cross-validator needs to be repeated.\nIt has to be an integer greater than 1."))        
        Nrepeatentry = customtkinter.CTkEntry(master=subframeRepeat, justify='center', placeholder_text=n_repeat.get())
        Nrepeatentry.pack(pady=6, padx=10, side='right')
        
        #random_state
        subframeRd = customtkinter.CTkFrame(subframe, width=200, height=100)
        subframeRd.pack(side="top", fill="both", padx=10, pady=6)

        labelRd = customtkinter.CTkLabel(subframeRd, text="Random state *")
        labelRd.pack(side="left", fill="both", padx=(10, 5))
        labelRd.bind("<Button-1>", lambda event : show_message("info","Controls the generation of the random states for each repetition.\nPass an int for reproducible output across multiple function calls."))        
        Rdentry = customtkinter.CTkEntry(master=subframeRd, justify='center', placeholder_text=cv_rd.get())
        Rdentry.pack(pady=6, padx=10, side='right')

        close_button = customtkinter.CTkButton(paramwindow, text="Close", command=paramwindow.destroy)
        close_button.pack(side="left", padx=(10, 5))
        
        def save_values():
            if len(Nsplitentry.get()) > 0:
                n_splits.set(Nsplitentry.get())
            if len(Nrepeatentry.get()) > 0:
                n_repeat.set(Nrepeatentry.get())
            if len(Rdentry.get()) > 0:
                cv_rd.set(Rdentry.get())   
            show_message("Info", "Your new parameters have been saved")
            
        save_button = customtkinter.CTkButton(paramwindow, text="Save", command=save_values)
        save_button.pack(side="right", padx=(5, 10))
    
    elif outersplitter.get() == 'GroupShuffleSplit':
        #n_splits
        subframeNsplit = customtkinter.CTkFrame(subframe, width=200, height=100)
        subframeNsplit.pack(side="top", fill="both", padx=10, pady=6)

        labelnsplit = customtkinter.CTkLabel(subframeNsplit, text="n_splits *")
        labelnsplit.pack(side="left", fill="both", padx=(10, 5))
        labelnsplit.bind("<Button-1>", lambda event : show_message("info","Number of folds in the cross validation. Must be at least 2.\nIt has to be an integer."))        
        Nsplitentry = customtkinter.CTkEntry(master=subframeNsplit, justify='center', placeholder_text=n_splits.get())
        Nsplitentry.pack(pady=6, padx=10, side='right')
        
        #test_size
        subframeTestsize = customtkinter.CTkFrame(subframe, width=200, height=100)
        subframeTestsize.pack(side="top", fill="both", padx=10, pady=6)

        labeltestsize = customtkinter.CTkLabel(subframeTestsize, text="test_size *")
        labeltestsize.pack(side="left", fill="both", padx=(10, 5))
        labeltestsize.bind("<Button-1>", lambda event : show_message("info","If float, should be between 0.0 and 1.0 and represent the proportion of groups to include in the test split (rounded up).\n\tIf int, represents the absolute number of test groups.\n\tIf None, the value is set to the complement of the train size.\nThe default value will remain 0.2 only if train_size is unspecified,\notherwise it will complement the specified train_size"))        
        Testsizeentry = customtkinter.CTkEntry(master=subframeTestsize, justify='center', placeholder_text=test_size.get())
        Testsizeentry.pack(pady=6, padx=10, side='right')
        
        #train_size
        subframeTrainsize = customtkinter.CTkFrame(subframe, width=200, height=100)
        subframeTrainsize.pack(side="top", fill="both", padx=10, pady=6)

        labeltrainsize = customtkinter.CTkLabel(subframeTrainsize, text="train_size *")
        labeltrainsize.pack(side="left", fill="both", padx=(10, 5))
        labeltrainsize.bind("<Button-1>", lambda event : show_message("info","If float, should be between 0.0 and 1.0 and represent the proportion of the groups to include in the train split.\nIf int, represents the absolute number of train groups.\nIf None, the value is automatically set to the complement of the test size."))        
        Trainsizeentry = customtkinter.CTkEntry(master=subframeTrainsize, justify='center', placeholder_text=train_size.get())
        Trainsizeentry.pack(pady=6, padx=10, side='right')
        
        #random_state
        subframeRd = customtkinter.CTkFrame(subframe, width=200, height=100)
        subframeRd.pack(side="top", fill="both", padx=10, pady=6)

        labelRd = customtkinter.CTkLabel(subframeRd, text="Random state *")
        labelRd.pack(side="left", fill="both", padx=(10, 5))
        labelRd.bind("<Button-1>", lambda event : show_message("info","Controls the generation of the random states for each repetition.\nPass an int for reproducible output across multiple function calls."))        
        Rdentry = customtkinter.CTkEntry(master=subframeRd, justify='center', placeholder_text=cv_rd.get())
        Rdentry.pack(pady=6, padx=10, side='right')

        close_button = customtkinter.CTkButton(paramwindow, text="Close", command=paramwindow.destroy)
        close_button.pack(side="left", padx=(10, 5))
        
        def save_values():
            if len(Nsplitentry.get()) > 0:
                n_splits.set(Nsplitentry.get())
            if len(Testsizeentry.get()) > 0:
                test_size.set(Testsizeentry.get())
            if len(Trainsizeentry.get()) > 0:
                train_size.set(Nrepeatentry.get())
            if len(Rdentry.get()) > 0:
                cv_rd.set(Rdentry.get())   
            show_message("Info", "Your new parameters have been saved")
            
        save_button = customtkinter.CTkButton(paramwindow, text="Save", command=save_values)
        save_button.pack(side="right", padx=(5, 10))
    else:
        error = customtkinter.CTkLabel(subframe, text="Outer splitter not recognised")
        error.pack(padx=10, pady=6)
        close_button = customtkinter.CTkButton(paramwindow, text="Close", command=paramwindow.destroy)
        close_button.pack(padx=20, pady=20)
        
    paramwindow.mainloop()


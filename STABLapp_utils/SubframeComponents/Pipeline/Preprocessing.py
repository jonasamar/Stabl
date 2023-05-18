#------------------------------------------------------------------------------------------------------------------------------
#
# Function : preprocess_activation
#
# Description :
#       - arguments : subframe, preprocess (Boolean)
#       - effect : Display a checkbox in which the user can activate or not a preprocessing step for the data before being fed
#                   to the model
#                  Update the variable preprocess with the value selected
#                  With version 3, there is the possibility of personalizing the preprocessing pipeline.
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter

from STABLapp_utils.subwindows.MessageWindow import show_message

def preprocess_activation(version, subframePipeline, preprocess):
    subframePrepro = customtkinter.CTkFrame(subframePipeline, width=200, height=100)
    subframePrepro.pack(side="top", fill="both", padx=10, pady=6)

    labelprepro = customtkinter.CTkLabel(subframePrepro, text="Preprocessing *")
    labelprepro.pack(side="left", fill="both", padx=(10, 5))

    def show_personalize_button():
        if preprocess.get():
            LabelDefault.pack_forget()
            subframePrepro.after(10, lambda: PersonalizeButton.pack(side="right", fill="both", padx=10, pady=5))
        else:
            PersonalizeButton.pack_forget()
            subframePrepro.after(10, lambda: LabelDefault.pack(side="right", padx=10, pady=5))
            
    if version == 'v1' or version == 'v2':
        checkboxprepro = customtkinter.CTkCheckBox(master=subframePrepro, variable=preprocess, text=None)
        checkboxprepro.pack(side="left", fill="both", padx=10, pady=5)
        labelprepro.bind("<Button-1>", lambda event : show_message("info","For now the default preprocessing is the following (you can activate it or deactivate it):\n\npreprocessing = Pipeline(\n\tsteps=[\n\t\t('lif', LowInfoFilter(0.2)),\n\t\t('variance', VarianceThreshold(0.01)),\n\t\t('impute', SimpleImputer(strategy='median')),\n\t\t('std', StandardScaler())\n\t]\n\nIt removes low informative features based on their variance and their proportion of missing values, standardize your data and finally replace the remaining missing values with the median of the feature (which won't bias your model)."))
    elif version == 'v3':
        checkboxprepro = customtkinter.CTkCheckBox(master=subframePrepro, variable=preprocess, text=None, command=show_personalize_button)
        checkboxprepro.pack(side="left", fill="both", padx=10, pady=5)
        labelprepro.bind("<Button-1>", lambda event : show_message("info","You can either have the preprocessing by default which:\n\t1 - Removes features of variance 0\n\t2 - Removes low info features (features with more than 20% of missing values)\n\t3 - Replaces the missing values by the median of the feature\n\t4 - Standardizes all the features\n\nOr, you can personalize your preprocessing."))
        
        PersonalizeButton = customtkinter.CTkButton(master=subframePrepro, text="Personalize preprocessing", command= lambda : personalize_pipeline())
        LabelDefault = customtkinter.CTkLabel(subframePrepro, text="(Default preprocessing *)", justify='left')
        LabelDefault.bind("<Button-1>", lambda event : show_message("info","The default preprocessing:\n\t1 - Removes features of variance 0\n\t2 - Removes low info features (features with more than 20% of missing values)\n\t3 - Replaces the missing values by the median of the feature\n\t4 - Standardizes all the features"))

        PersonalizeButton.pack(side="right", fill="both", padx=10, pady=5)


def personalize_pipeline():
            
    window = customtkinter.CTk()
    window.geometry("700x400")
    window.title('Preprocessing personalization')
    
    intro = customtkinter.CTkLabel(window, text=f"Here are the different functions you can put in your preprocessing.\nOnce selected, you can specify the parameters of each function to personalize your preprocessing.\nYou can also deactivate functions.")
    intro.pack(padx=10, pady=10)
    
    subframe = customtkinter.CTkFrame(window, width=200, height=100)
    subframe.pack(side="top", fill="both", padx=10, pady=6)
        
    #Variance
    subframeVar = customtkinter.CTkFrame(subframe, width=200, height=100)
    subframeVar.pack(side="top", fill="both", padx=10, pady=6)
    
    checkboxVar = customtkinter.CTkCheckBox(master=subframeVar, text='Removing features with variance under threshold')
    checkboxVar.pack(side="left", padx=(10, 5))
    Varentry = customtkinter.CTkEntry(master=subframeVar, justify='center', placeholder_text='0.01')
    Varentry.pack(pady=6, padx=(5,10), side='right')
    
    #Variance
    subframeVar = customtkinter.CTkFrame(subframe, width=200, height=100)
    subframeVar.pack(side="top", fill="both", padx=10, pady=6)
    
    checkboxVar = customtkinter.CTkCheckBox(master=subframeVar, text='Removing features with variance under threshold')
    checkboxVar.pack(side="left", padx=(10, 5))
    Varentry = customtkinter.CTkEntry(master=subframeVar, justify='center', placeholder_text='0.01')
    Varentry.pack(pady=6, padx=(5,10), side='right')
    
    #Variance
    subframeVar = customtkinter.CTkFrame(subframe, width=200, height=100)
    subframeVar.pack(side="top", fill="both", padx=10, pady=6)
    
    checkboxVar = customtkinter.CTkCheckBox(master=subframeVar, text='Removing features with variance under threshold')
    checkboxVar.pack(side="left", padx=(10, 5))
    Varentry = customtkinter.CTkEntry(master=subframeVar, justify='center', placeholder_text='0.01')
    Varentry.pack(pady=6, padx=(5,10), side='right')
    
    #Variance
    subframeVar = customtkinter.CTkFrame(subframe, width=200, height=100)
    subframeVar.pack(side="top", fill="both", padx=10, pady=6)
    
    checkboxVar = customtkinter.CTkCheckBox(master=subframeVar, text='Removing features with variance under threshold')
    checkboxVar.pack(side="left", padx=(10, 5))
    Varentry = customtkinter.CTkEntry(master=subframeVar, justify='center', placeholder_text='0.01')
    Varentry.pack(pady=6, padx=(5,10), side='right')
    
    close_button = customtkinter.CTkButton(window, text="Close", command=window.destroy)
    close_button.pack(side="left", padx=(10, 5))

    def save_values():
        show_message("Info", "Your new parameters have been saved")
                    
    save_button = customtkinter.CTkButton(window, text="Save", command=save_values)
    save_button.pack(side="right", padx=(5, 10))

    window.mainloop()
    
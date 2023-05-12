import customtkinter
from subwindows import show_message

def preprocess_activation(subframePipeline, preprocess):
    subframePrepro = customtkinter.CTkFrame(subframePipeline, width=200, height=100)
    subframePrepro.pack(side="top", fill="both", padx=10, pady=6)

    labelprepro = customtkinter.CTkLabel(subframePrepro, text="Preprocessing *")
    labelprepro.pack(side="left", fill="both", padx=(10, 5))
    labelprepro.bind("<Button-1>", lambda event : show_message("info","For now the default preprocessing is the following (you can activate it or deactivate it):\n\npreprocessing = Pipeline(\n\tsteps=[\n\t\t('lif', LowInfoFilter(0.2)),\n\t\t('variance', VarianceThreshold(0.01)),\n\t\t('impute', SimpleImputer(strategy='median')),\n\t\t('std', StandardScaler())\n\t]\n\nIt removes low informative features based on their variance and their proportion of missing values, standardize your data and finally replace the remaining missing values with the median of the feature (which won't bias your model)."))

    checkboxprepro = customtkinter.CTkCheckBox(master=subframePrepro, variable=preprocess, text=None)
    checkboxprepro.pack(side="left", fill="both", padx=10, pady=5)
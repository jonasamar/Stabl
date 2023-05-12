import customtkinter
from subwindows import show_message 

def sample_fraction_tuning(subframeStabl, sample_fraction):
    subframeFrac = customtkinter.CTkFrame(subframeStabl, width=200, height=100)
    subframeFrac.pack(side="top", fill="both", padx=10, pady=6)
    
    labelval = customtkinter.CTkLabel(subframeFrac, textvariable=sample_fraction)
    labelval.pack()

    labelfrac = customtkinter.CTkLabel(subframeFrac, text="Sample fraction *")
    labelfrac.pack(side="left", fill="both", padx=(10, 5))
    labelfrac.bind("<Button-1>", lambda event : show_message("info","STABL is one model but it is powerful because it relies on the construction of 1000 'submodels'.\n All these 'submodels' have the same nature (they are all ElasticNet models with the same l1_ratio you have chosen) but they are trained on different datasets.\n\n Each 'submodel' is trained on a bootstrap of your dataset which is a portion of this dataset.\nThe sample fraction corresponds to the proportion of the training dataset which is used in each bootstrap."))

    fracscale = customtkinter.CTkSlider(subframeFrac, from_=0., to=2., orientation='horizontal', variable=sample_fraction, number_of_steps=20, width=550)
    fracscale.pack(side="left", fill="both", padx=10, pady=5)
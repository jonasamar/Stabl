import customtkinter

from subwindows import show_message

# Main frame
def subframeStabl_display(root, ratioval, artificial_type, sample_fraction, replace, random_state):
    subframeStabl = customtkinter.CTkFrame(root, width=200, height=100)
    subframeStabl.pack(side="top", fill="both", padx=10, pady=6)
    
    labelStabl = customtkinter.CTkLabel(subframeStabl, text="Stabl : fine tuning")
    labelStabl.pack(pady=0, padx=10)
    
    l1_ratio_tuning(subframeStabl, ratioval)
    artificial_type_choice(subframeStabl, artificial_type)
    sample_fraction_tuning(subframeStabl, sample_fraction)
    replace_tuning(subframeStabl, replace)
    random_state_tuning(subframeStabl, random_state)

    FinerTuningButton = customtkinter.CTkButton(master=subframeStabl, text="For even finer tuning...", command= lambda : stabl_fine_tuning())
    FinerTuningButton.pack(pady=12, padx=10)

# Components
def l1_ratio_tuning(subframeStabl, ratioval):
    subframeRatio = customtkinter.CTkFrame(subframeStabl, width=200, height=100)
    subframeRatio.pack(side="top", fill="both", padx=10, pady=6)
    
    labelval = customtkinter.CTkLabel(subframeRatio, textvariable=ratioval)
    labelval.pack()

    labelratio = customtkinter.CTkLabel(subframeRatio, text="L1 Ratio *")
    labelratio.pack(side="left", fill="both", padx=(10, 5))
    labelratio.bind("<Button-1>", lambda event : show_message("info","This ratio correspond to how sparse you want your model.\n\n\t* If the ratio = 1., a l1 penalty is applied (lasso model) which will give the sparsest model. \n\n\t* If the ratio = 0., a l2 penalty is applied (ridge regression model) corresponding to the least sparse model.\n\nThe values in between correspond to models whose sparsity are between these extrem models."))

    ratioscale = customtkinter.CTkSlider(subframeRatio, from_=0., to=1., orientation='horizontal', variable=ratioval, number_of_steps=50, width=550)
    ratioscale.pack(side="left", fill="both", padx=10, pady=5)
    
def artificial_type_choice(subframeStabl, artificial_type):
    subframeArti = customtkinter.CTkFrame(subframeStabl, width=200, height=100)
    subframeArti.pack(side="top", fill="both", padx=10, pady=6)
    
    labelarti = customtkinter.CTkLabel(subframeArti, text="Artificial type *")
    labelarti.pack(side="left", fill="both", padx=(10, 5))
    labelarti.bind("<Button-1>", lambda event : show_message("info","One of the first step in the STABL pipeline is to generate random features that we know are not interesting.\nThese features help STABL select the best FDR (false discovery rate) threshold possible (because they allow us to calculate a good estimate of the false discovery proportion : FDP+)).\n\nThe two strategies to generate these random features are random_permutation and knockoff. You can try both strategies and compare the results to see which one seems the most appropriate to your study."))
                   
    comboboxarti = customtkinter.CTkComboBox(subframeArti, variable=artificial_type, values=["random_permutation", "knockoff"], width=300)
    comboboxarti.pack(side="left", fill="both", padx=10, pady=5)

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
    
def replace_tuning(subframeStabl, replace):
    subframeRepl = customtkinter.CTkFrame(subframeStabl, width=200, height=100)
    subframeRepl.pack(side="top", fill="both", padx=10, pady=6)

    labelrepl = customtkinter.CTkLabel(subframeRepl, text="Replace *")
    labelrepl.pack(side="left", fill="both", padx=(10, 5))
    labelrepl.bind("<Button-1>", lambda event : show_message("info","The way each bootstrap is built is by extracting a certain number or proportion of samples from your original dataset.\nThere are two ways of extracting those samples :\n\n\n\n\t* WITH replacement (Replace=True) : each time you select one sample from your original dataset to build your bootstrap, you replace it.\n\n\t(example : If you are doing a bootstrap of two cards within a deck of 52 cards with replacement, you would \n\t\t(1) pick a first card \n\t\t(2) pick a second card in another copy of your entire deck (you would still have 52 choices because you are picking a card from a brand new deck).\n\tConsequently you can pick twice the same card)\n\n\tThus, bootstraps with replacement can contain multiple copies of the same sample.\n\tThis kind of bootstrap becomes interesting when you have a low number of samples and a sample proportion close to 1. or greater than 1.\n\n\n\n\t* WITHOUT replacement (Replace=False) : each time you select one sample from your original dataset to build your bootstrap, you DON'T replace it.\n\n\t(example : If you are doing a bootstrap of two cards within a deck of 52 cards WITHOUT replacement, you would \n\t\t(1) pick a first card \n\t\t(2) pick a second card in the same deck (you would only have 51 choices because you already took one out).\n\tConsequently you CANNOT pick twice the same card)\n\n\tThus, bootstraps with replacement CANNOT contain multiple copies of the same sample.\n\tThis kind of bootstrap becomes interesting when you have a sample proportion close to 0.5"))

    checkboxrepl = customtkinter.CTkCheckBox(master=subframeRepl, variable=replace, text=None)
    checkboxrepl.pack(side="left", fill="both", padx=10, pady=5)

def random_state_tuning(subframeStabl, random_state):
    subframeRand = customtkinter.CTkFrame(subframeStabl, width=200, height=100)
    subframeRand.pack(side="top", fill="both", padx=10, pady=6)
    
    labelval = customtkinter.CTkLabel(subframeRand, textvariable=random_state)
    labelval.pack()

    labelrand = customtkinter.CTkLabel(subframeRand, text="Random State *")
    labelrand.pack(side="left", fill="both", padx=(10, 5))
    labelrand.bind("<Button-1>", lambda event : show_message("info","Random state is the random seed used to initialize some values in the STABL pipeline.\nIt has to be an integer.\nIts value won't change drastically the performances of your model but you can try different values to take the best initialization possible for your model/ study."))

    randscale = customtkinter.CTkSlider(subframeRand, from_=0, to=100, orientation='horizontal', variable=random_state, number_of_steps=101, width=550)
    randscale.pack(side="left", fill="both", padx=10, pady=5)

def stabl_fine_tuning():
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("dark-blue")
    
    window = customtkinter.CTk()
    
    window.title('For even finer tuning...')
    label = customtkinter.CTkLabel(window, text='# TO DO !')
    label.pack(padx=20, pady=20)
    close_button = customtkinter.CTkButton(window, text="Close", command=window.destroy)
    close_button.pack(padx=20, pady=20)
    window.mainloop()
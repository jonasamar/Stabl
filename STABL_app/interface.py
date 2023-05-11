import customtkinter
import tkinter
from tkinter import ttk
from script_utils import python_script
from subwindows import show_message

def main():
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()
    root.geometry("600x800")
    root.title("STABL interface")

    label = customtkinter.CTkLabel(master=root, text="Creation of python & sbatch scripts", font=("Roboto", 20)) 
    label.pack(pady=6, padx=10)

    foldername = customtkinter.CTkEntry(master=root, width=200, justify='center', placeholder_text="STABL Run Name")
    foldername.pack(pady=6, padx=10)

    ### Subframe 1 : Python File Settings
    label1 = customtkinter.CTkLabel(master=root, text="Python File Settings", font=("Roboto", 15)) 
    label1.pack(pady=6, padx=10)

    subframe1 = customtkinter.CTkFrame(master=root)
    subframe1.pack(side="top", fill="both", pady=6, padx=10)

    # Data File informations
    X_file = customtkinter.StringVar()
    y_col = customtkinter.StringVar()
    y_file = customtkinter.StringVar()
    data_entry(subframe1, X_file, y_col, y_file)

    # Stabl fine tuning
    subframeStabl = customtkinter.CTkFrame(root, width=200, height=100)
    subframeStabl.pack(side="top", fill="both", padx=10, pady=6)
    
    labelStabl = customtkinter.CTkLabel(subframeStabl, text="Stabl : fine tuning")
    labelStabl.pack(pady=0, padx=10)
    
    ratioval = customtkinter.DoubleVar(value='0.5')
    l1_ratio_tuning(subframeStabl, ratioval)
    
    artificial_type = customtkinter.StringVar(value='random_permutation')
    artificial_type_choice(subframeStabl, artificial_type)
    
    sample_fraction = customtkinter.DoubleVar(value='0.5')
    sample_fraction_tuning(subframeStabl, sample_fraction)
    
    


    ### Subframe 3 : Sbatch File Settings
    # subframe3 = customtkinter.CTkFrame(master=root)
    # subframe3.pack(pady=15, padx=20, fill="both", expand=True)

    # label3 = customtkinter.CTkLabel(master=root, text="Sbatch File Settings", font=("Roboto", 15)) 
    # label3.pack(pady=12, padx=10)

    CreationButton = customtkinter.CTkButton(master=root, text="Create", command= lambda : python_script(foldername.get(), X_file.get(), y_col.get(), y_file.get(), ratioval.get(), artificial_type.get(), sample_fraction.get()))
    CreationButton.pack(pady=12, padx=10)

    # checkbox = customtkinter.CTkCheckBox(master=frame, text="Remember Me")
    # checkbox.pack(pady=12, padx=10)

    root.mainloop()

def data_entry(subframe1, X_file, y_col, y_file,):
    subframeX = customtkinter.CTkFrame(subframe1, width=200, height=100)
    subframeX.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
    subframeColY = customtkinter.CTkFrame(subframe1, width=200, height=100)
    subframeColY.pack(side="left", fill="both", expand=True, padx=5, pady=10)
    subframeY = customtkinter.CTkFrame(subframe1, width=200, height=100)
    subframeY.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)

    labelX = customtkinter.CTkLabel(subframeX, text="Datafile Name *")
    labelX.pack()
    labelX.bind("<Button-1>", lambda event : show_message("info", "The name you enter should correspond to the file with your entire dataset."))
    datafileX = customtkinter.CTkEntry(master=subframeX, textvariable = X_file, justify='center', placeholder_text="None")
    datafileX.pack(pady=6, padx=10)

    labelColY = customtkinter.CTkLabel(subframeColY, text="Outcome column *")
    labelColY.pack()
    labelColY.bind("<Button-1>", lambda event : show_message("info","If the file containing your entire dataset also contains the outcome you want to predict, you have to specify the name of the column corresponding to your outcome. Otherwise, leave this text box blank."))
    ColY = customtkinter.CTkEntry(master=subframeColY, textvariable=y_col, justify='center', placeholder_text="None")
    ColY.pack(pady=6, padx=10)

    labelY = customtkinter.CTkLabel(subframeY, text="Outcome file *")
    labelY.pack()
    labelY.bind("<Button-1>", lambda event : show_message("info","If you have a distinct file with the outcome you want to predict, enter the name of the file in this text box. Otherwise, leave this text box blank."))
    datafileY = customtkinter.CTkEntry(master=subframeY, textvariable=y_file, justify='center', placeholder_text="None")
    datafileY.pack(pady=6, padx=10)


def l1_ratio_tuning(subframeStabl, ratioval):
    subframeRatio = customtkinter.CTkFrame(subframeStabl, width=200, height=100)
    subframeRatio.pack(side="top", fill="both", padx=10, pady=6)
    
    labelval = customtkinter.CTkLabel(subframeRatio, textvariable=ratioval)
    labelval.pack()

    labelratio = customtkinter.CTkLabel(subframeRatio, text="L1 Ratio *")
    labelratio.pack(side="left", fill="both", padx=(10, 5))
    labelratio.bind("<Button-1>", lambda event : show_message("info","This ratio correspond to how sparse you want your model.\n\nIf the ratio = 1., a l1 penalty is applied (lasso model) which will give the sparsest model. \n\nIf the ratio = 0., a l2 penalty is applied (ridge regression model) corresponding to the least sparse model.\n\nThe values in between correspond to models whose sparsity are between these extrem models."))

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
    
    labelfrac = customtkinter.CTkLabel(subframeFrac, textvariable=sample_fraction)
    labelfrac.pack()

    labelfrac = customtkinter.CTkLabel(subframeFrac, text="Sample fraction *")
    labelfrac.pack(side="left", fill="both", padx=(10, 5))
    labelfrac.bind("<Button-1>", lambda event : show_message("info","STABL is one model but it is powerful because it relies on the construction of 1000 'submodels'.\n All these 'submodels' have the same nature (they are all ElasticNet models with the same l1_ratio you have chosen) but they are trained on different datasets.\n\n Each 'submodel' is trained on a bootstrap of your dataset which is a portion of this dataset.\nThe sample fraction corresponds to the proportion of the training dataset which is used in each bootstrap."))

    fracscale = customtkinter.CTkSlider(subframeFrac, from_=0., to=2., orientation='horizontal', variable=sample_fraction, number_of_steps=20, width=550)
    fracscale.pack(side="left", fill="both", padx=10, pady=5)
    
main()

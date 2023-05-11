import customtkinter
# import tkinter
# from tkinter import ttk

from subframeData import subframeData_display
from subframeStabl import subframeStabl_display
from subframePipeline import subframePipeline_display
from script_utils import python_script
from subwindows import show_message

def main():
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()
    root.geometry("1200x800")
    root.title("STABL interface")
    
    # Variables : 
    X_file = customtkinter.StringVar()
    y_col = customtkinter.StringVar()
    y_file = customtkinter.StringVar()
    
    ratioval = customtkinter.DoubleVar(value='1.')
    artificial_type = customtkinter.StringVar(value='random_permutation')
    sample_fraction = customtkinter.DoubleVar(value='0.5')
    replace = customtkinter.BooleanVar(value=False)
    random_state = customtkinter.IntVar(value=42)
    
    preprocess = customtkinter.BooleanVar(value=True)
    
    outersplitter = customtkinter.StringVar(value='RepeatedStratifiedKFold')
    n_splits = customtkinter.IntVar(value=5)
    n_repeat = customtkinter.IntVar(value=10)
    cv_rd = customtkinter.IntVar(value=42)
    test_size = customtkinter.DoubleVar(value=0.2)
    train_size = customtkinter.DoubleVar(value=None)
    
    # Main Window
    label = customtkinter.CTkLabel(master=root, text="Creation of python & sbatch scripts", font=("Roboto", 20)) 
    label.pack(pady=6, padx=10)
    
    leftpanel = customtkinter.CTkFrame(root, width=200, height=100)
    leftpanel.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
    
    rightpanel = customtkinter.CTkFrame(root, width=200, height=100)
    rightpanel.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)

    foldername = customtkinter.CTkEntry(master=leftpanel, width=200, justify='center', placeholder_text="STABL Run Name")
    foldername.pack(pady=6, padx=10)
    
    ### Python File Settings
    label1 = customtkinter.CTkLabel(master=leftpanel, text="Python File Settings", font=("Roboto", 15)) 
    label1.pack(pady=6, padx=10)

    ## Left Panel
    # Data File informations
    subframeData_display(leftpanel, X_file, y_col, y_file)
    # Stabl Pipeline informations
    subframePipeline_display(leftpanel, preprocess, outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size)

    ## Right Panel
    # Stabl fine tuning
    subframeStabl_display(rightpanel, ratioval, artificial_type, sample_fraction, replace, random_state)
    
    ### Subframe 3 : Sbatch File Settings
    # subframe3 = customtkinter.CTkFrame(master=root)
    # subframe3.pack(pady=15, padx=20, fill="both", expand=True)

    # label3 = customtkinter.CTkLabel(master=root, text="Sbatch File Settings", font=("Roboto", 15)) 
    # label3.pack(pady=12, padx=10)

    CreationButton = customtkinter.CTkButton(master=root, text="Create", command= lambda : python_script(foldername.get(), X_file.get(), y_col.get(), y_file.get(), ratioval.get(), artificial_type.get(), sample_fraction.get(), replace.get(), random_state.get(), preprocess.get(), outersplitter.get(), n_splits.get(), n_repeat.get(), cv_rd.get(), test_size.get(), train_size.get()))
    CreationButton.pack(pady=12, padx=10)

    # checkbox = customtkinter.CTkCheckBox(master=frame, text="Remember Me")
    # checkbox.pack(pady=12, padx=10)

    root.mainloop()
    
main()

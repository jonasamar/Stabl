import customtkinter
# import tkinter
# from tkinter import ttk

from subframeData import subframeData_display
from subframeStabl import subframeStabl_display
from subframePipeline import subframePipeline_display
from subframeSbatch import subframeSbatch_display

from script_utils import write_scripts

def main():
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()
    root.geometry("1350x800")
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
    
    pipeline = customtkinter.StringVar(value='single_omic_stabl_cv')
    task_type = customtkinter.StringVar(value='binary')
    
    outer_groups = customtkinter.StringVar(value=None)
    X_test = customtkinter.StringVar(value=None)
    y_test_col = customtkinter.StringVar(value=None)
    y_test = customtkinter.StringVar(value=None)
    
    days = customtkinter.StringVar(value="2")
    hours = customtkinter.StringVar(value="00")
    minutes = customtkinter.StringVar(value="00")
    sec = customtkinter.StringVar(value="00")
    nb_cpu = customtkinter.StringVar(value="2")
    mem_cpu = customtkinter.StringVar(value="16 GB")
    
    # Main Window
    label = customtkinter.CTkLabel(master=root, text="Creation of python & sbatch scripts", font=("Roboto", 20)) 
    label.pack(pady=6, padx=10)
    
    leftpanel = customtkinter.CTkFrame(root, width=200, height=100)
    leftpanel.pack(side="left", fill='both', padx=(10, 5), pady=10)
    
    rightpanel = customtkinter.CTkFrame(root, width=200, height=100)
    rightpanel.pack(side="left", fill='both', padx=(5, 10), pady=10)

    foldername = customtkinter.CTkEntry(master=leftpanel, width=200, justify='center', placeholder_text="STABL Run Name")
    foldername.pack(pady=6, padx=10)
    
    ### Python File Settings
    label1 = customtkinter.CTkLabel(master=leftpanel, text="Python File Settings", font=("Roboto", 16)) 
    label1.pack(pady=6, padx=10)

    subframeData_display(leftpanel, X_file, y_col, y_file)
    subframePipeline_display(leftpanel, preprocess, outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size, pipeline, task_type, outer_groups, X_test, y_test_col, y_test)
    subframeStabl_display(rightpanel, ratioval, artificial_type, sample_fraction, replace, random_state)
    subframeSbatch_display(rightpanel, days, hours, minutes, sec, nb_cpu, mem_cpu)
    
    CreationButton = customtkinter.CTkButton(master=rightpanel, text="Create", command= lambda : write_scripts(foldername.get(), X_file.get(), y_col.get(), y_file.get(), ratioval.get(), artificial_type.get(), sample_fraction.get(), replace.get(), random_state.get(), preprocess.get(), outersplitter.get(), n_splits.get(), n_repeat.get(), cv_rd.get(), test_size.get(), train_size.get(), pipeline.get(), task_type.get(), outer_groups.get(), X_test.get(), y_test_col.get(), y_test.get(), days.get(), hours.get(), minutes.get(), sec.get(), nb_cpu.get(), mem_cpu.get()))
    CreationButton.pack(side="top", pady=12, padx=10)

    root.mainloop()
    
main()

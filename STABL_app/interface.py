import tkinter
import customtkinter
from script_utils import test_script

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("600x800")
root.title("STABL interface")

### Main Frame
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Creation of python & sbatch scripts", font=("Roboto", 20)) 
label.pack(pady=12, padx=10)

### Subframe 1 : General information
subframe1 = customtkinter.CTkFrame(master=frame)
subframe1.pack(pady=15, padx=20, fill="both", expand=True)

foldername = customtkinter.CTkEntry(master=subframe1, width=200, justify='center', placeholder_text="STABL Run Name")
foldername.pack(pady=12, padx=10)

### Subframe 2 : Python File Settings
subframe2 = customtkinter.CTkFrame(master=frame)
subframe2.pack(pady=15, padx=20, fill="both", expand=True)

label2 = customtkinter.CTkLabel(master=frame, text="Python File Settings", font=("Roboto", 15)) 
label2.pack(pady=12, padx=10)

answer1 = customtkinter.StringVar()
dropdown1 = customtkinter.CTkCombobox(subframe2, values=["Single omic pipeline", "Multi omic pipeline"], textvariable=answer1)
dropdown1.pack()

datafilename = customtkinter.CTkEntry(master=subframe2, width=200, justify='center', placeholder_text="Data file name")
datafilename.pack(pady=12, padx=10)

### Subframe 3 : Sbatch File Settings
subframe3 = customtkinter.CTkFrame(master=frame)
subframe3.pack(pady=15, padx=20, fill="both", expand=True)

label3 = customtkinter.CTkLabel(master=frame, text="Sbatch File Settings", font=("Roboto", 15)) 
label3.pack(pady=12, padx=10)

CreationButton = customtkinter.CTkButton(master=frame, text="Create", command= lambda : test_script(foldername.get()))
CreationButton.pack(pady=12, padx=10)

# checkbox = customtkinter.CTkCheckBox(master=frame, text="Remember Me")
# checkbox.pack(pady=12, padx=10)

root.mainloop()



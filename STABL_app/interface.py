import tkinter
import customtkinter
from script_utils import test_script
from subwindows import show_message

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
subframeX = customtkinter.CTkFrame(subframe1, width=200, height=100)
subframeX.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
subframeColY = customtkinter.CTkFrame(subframe1, width=200, height=100)
subframeColY.pack(side="left", fill="both", expand=True, padx=5, pady=10)
subframeY = customtkinter.CTkFrame(subframe1, width=200, height=100)
subframeY.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)

labelX = customtkinter.CTkLabel(subframeX, text="Datafile Name *")
labelX.pack()
labelX.bind("<Button-1>", lambda event : show_message("info", "The name you enter should correspond to the file with your entire dataset."))
datafileX = customtkinter.CTkEntry(master=subframeX, justify='center', placeholder_text="None")
datafileX.pack(pady=6, padx=10)

labelColY = customtkinter.CTkLabel(subframeColY, text="Outcome column *")
labelColY.pack()
labelColY.bind("<Button-1>", lambda event : show_message("info","If the file containing your entire dataset also contains the outcome you want to predict, you have to specify the name of the column corresponding to your outcome. Otherwise, leave this text box blank."))
ColY = customtkinter.CTkEntry(master=subframeColY, justify='center', placeholder_text="None")
ColY.pack(pady=6, padx=10)

labelY = customtkinter.CTkLabel(subframeY, text="Outcome file *")
labelY.pack()
labelY.bind("<Button-1>", lambda event : show_message("info","If you have a distinct file with the outcome you want to predict, enter the name of the file in this text box. Otherwise, leave this text box blank."))
datafileY = customtkinter.CTkEntry(master=subframeY, justify='center', placeholder_text="None")
datafileY.pack(pady=6, padx=10)

### Subframe 3 : Sbatch File Settings
# subframe3 = customtkinter.CTkFrame(master=root)
# subframe3.pack(pady=15, padx=20, fill="both", expand=True)

# label3 = customtkinter.CTkLabel(master=root, text="Sbatch File Settings", font=("Roboto", 15)) 
# label3.pack(pady=12, padx=10)

CreationButton = customtkinter.CTkButton(master=root, text="Create", command= lambda : test_script(foldername.get(), datafileX.get(), ColY.get(), datafileY.get()))
CreationButton.pack(pady=12, padx=10)

# checkbox = customtkinter.CTkCheckBox(master=frame, text="Remember Me")
# checkbox.pack(pady=12, padx=10)

root.mainloop()



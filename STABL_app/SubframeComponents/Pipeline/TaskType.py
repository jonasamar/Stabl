#------------------------------------------------------------------------------------------------------------------------------
#
# Function : task_type_display
#
# Description :
#       - arguments : subframe, task_type
#       - effect : Display a combobox in which the user can select the type of task he or she expects from the model ('binary'
#                   or 'regression')
#                  Update the variable task_type with the value selected
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter

from subwindows.MessageWindow import show_message

def task_type_display(subframe, task_type):
    subframettype = customtkinter.CTkFrame(subframe, width=200, height=100)
    subframettype.pack(side="top", fill="both", padx=10, pady=6)
    
    labelttype = customtkinter.CTkLabel(subframettype, text="Task type *")
    labelttype.pack(side="left", fill="both", padx=(10, 5))
    labelttype.bind("<Button-1>", lambda event : show_message("info","binary : you have a classification problem and you want to predict 0 or 1 for a given sample.\n\nregression : you want to predict a value that takes a continous range of values (between  0 and 1 for instance)."))
    
    def update_task_type(event):
        print("Function")
        if comboboxttype.get() == "binary":
            task_type.set("binary")
            print(task_type.get())
        elif comboboxttype.get() == "continuous":
            task_type.set("regression")
            print(task_type.get())

    comboboxttype = customtkinter.CTkComboBox(subframettype, values=["binary", "continuous"], width=150, command=update_task_type)
    comboboxttype.pack(side="left", fill="both", padx=10, pady=5)
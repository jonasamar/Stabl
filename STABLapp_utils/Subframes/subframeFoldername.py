#------------------------------------------------------------------------------------------------------------------------------
#
# Function : subframeFoldername_display
#
# Description :
#       - arguments : leftpanel, foldername, file_list
#       - effect : Display an entry textbox to put the name of the project (or folder) and change the entry textbox into a
#                   label when file_list contains elements to make sure the user doesn't change the name of the folder in the
#                   middle of the process (otherwise some files would be imported in different folders...)
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter

def subframeFoldername_display(leftpanel, foldername, file_list):
    subframeFoldername = customtkinter.CTkFrame(leftpanel, width=200, height=100, border_color="black")
    subframeFoldername.pack(pady=6, padx=10, fill='both')
    labelFoldername = customtkinter.CTkLabel(subframeFoldername, text="Project name : ", font=("Roboto", 14)) 
    labelFoldername.pack(pady=6, padx=10, side='left')
    foldername_text = customtkinter.CTkEntry(master=subframeFoldername, width=200, justify='center',textvariable=foldername,  placeholder_text="STABL Run Name")
    foldername_text.pack(pady=6, padx=10, side='left')
    labelfoldername = customtkinter.CTkLabel(master=subframeFoldername, justify='left', textvariable=foldername, font=("Roboto", 14, "bold"))


    def update_foldername_label(*args):
        if len(file_list.get()) == 0:
            foldername_text.pack(pady=6, padx=10, side='left')
            labelfoldername.pack_forget()
        else:
            foldername_text.pack_forget()
            labelfoldername.pack(pady=6, padx=10, side='left')

    file_list.trace('w', lambda *args: update_foldername_label())
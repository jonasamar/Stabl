#------------------------------------------------------------------------------------------------------------------------------
#
# Function : delete_file
#
# Description :
#       - arguments : foldername (project directory), file_list,  subframes where we want to prompt the files names and types
#       - effect : Allow the user to navigate in the folder the app has created for his or her project and delete one of the 
#                   files.
#                  Update the value of file_list by removing the selected file
#                  Update the file display by refreshing the display of the files on the main window
#
#------------------------------------------------------------------------------------------------------------------------------

import os
import re

from customtkinter import CTkLabel, filedialog

from STABLapp_utils.subwindows.MessageWindow import show_message

def delete_file(foldername, 
                file_list, 
                subframeName, subframeType, subframeSpe):
    
    if has_special_chars_or_spaces(foldername) or len(foldername) == 0:
        show_message("Error", "Your STABL Run Name contains undesired characters or spaces or is empty.\nPlease chose another name before importing your data.")
    else:
        file_path = filedialog.askopenfilename(initialdir='./'+foldername, title="Select file to delete")
        if file_path:
            try:
                # Deleting the file from the project folder
                filename = os.path.basename(file_path)
                os.remove(file_path)
                # Updating file_list by removing the deleted file from the list
                delete(filename, file_list)
                files = str(file_list.get()).split('\n')
                # Delete previous display
                for widget in subframeName.winfo_children():
                    widget.destroy()
                for widget in subframeType.winfo_children():
                    widget.destroy()
                for widget in subframeSpe.winfo_children():
                    widget.destroy()
                # Create new display
                labelName = CTkLabel(master=subframeName, text="File name", font=("Roboto", 12, "bold"))
                labelName.pack(padx = 10, pady=3)
                labelType = CTkLabel(master=subframeType, text="Type of data", font=("Roboto", 12, "bold"))
                labelType.pack(padx = 10, pady=3)
                labelSpe = CTkLabel(master=subframeSpe, text="Type of features", font=("Roboto", 12, "bold"))
                labelSpe.pack(padx = 10, pady=3)
                for file in files:
                    display_file(subframeName, subframeType, subframeSpe, file)
            except OSError as e:
                show_message("Error", f"Error deleting file '{file_path}': {e}")
                
def display_file(subframeName, subframeType, subframeSpe, file):
    if len(file) > 0:
        elements = file.split('\t')
        name, datatype, spe = elements[0], elements[2], elements[3]
        labelname = CTkLabel(master=subframeName, text=name) 
        labelname.pack(side='top', fill='both', padx = 5, pady=5)
        labeltype = CTkLabel(master=subframeType, text=datatype) 
        labeltype.pack(side='top', fill='both', padx = 5, pady=5)
        labelspe = CTkLabel(master=subframeSpe, text=spe) 
        labelspe.pack(side='top', fill='both', padx = 5, pady=5)


def delete(filename, file_list):
    f_list = str(file_list.get()).split('\n')
    new_list = []
    for i in range(len(f_list)):
        if not filename in f_list[i]:
            new_list.append(f_list[i]+'\n')
    file_list.set(''.join(new_list))

def has_special_chars_or_spaces(input_string):
    pattern = re.compile('[^A-Za-z0-9]+') 
    return bool(pattern.search(input_string))
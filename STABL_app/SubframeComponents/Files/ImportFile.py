#------------------------------------------------------------------------------------------------------------------------------
#
# Function : add_file_and_display_files
#
# Description :
#       - arguments : foldername (project directory), file_list,  subframes where we want to prompt the files names and types
#       - effect : Allow the user to navigate in his computer office and add a file to the project folder.
#                  Update the value of file_list by adding the selected file
#                  Update the file display by refreshing the display of the files on the main window
#
#------------------------------------------------------------------------------------------------------------------------------

import os
import shutil
import re

from customtkinter import CTkEntry, CTkButton, CTkLabel, filedialog, CTkFrame, CTk, CTkComboBox

from subwindows.MessageWindow import show_message

def add_file_and_display_files(foldername, 
                               file_list, 
                               subframeName, subframeType, subframeSpe):
    
    if has_special_chars_or_spaces(foldername) or len(foldername) == 0:
        show_message("Error", "Your STABL Run Name contains undesired characters or spaces or is empty.\nPlease chose another name before importing your data.")
    else:
        source_file_path = filedialog.askopenfilename(title="Select file")
        
        # Creation of the folder if it does not exist
        if not os.path.exists(foldername):
            os.makedirs(foldername)
        
        # Copy and transfer of the file to the project folder
        filename = os.path.basename(source_file_path)
        if filename[-4:] != '.csv':
            show_message("Error", "This is not a csv file. Please convert it to a csv file before importing it.")
        else:
            file_list.set(file_list.get()+str(filename)+'\t') # updating the file list
            destination_file_path = os.path.join(foldername, filename)
            shutil.copy(source_file_path, destination_file_path)
            add_info_file(file_list, subframeName, subframeType, subframeSpe)

def add_info_file(file_list, 
                  subframeName, subframeType, subframeSpe): 
       
    root = CTk()
    root.geometry("400x300")
    root.title("What file have just imported ?")
    
    file = str(file_list.get()).split('\n')[-1][:-1]
    
    label = CTkLabel(master=root, text=f"You have decided to import {file}.\nPlease specify the type of information it contains") 
    label.pack(side='top', padx = 10, pady=10)
    
    # Type of data
    subframeDataType = CTkFrame(root, width=200, height=100)
    subframeDataType.pack(side="top", fill="both", padx=10, pady=6)
    labelDataType = CTkLabel(subframeDataType, text="This file contains *")
    labelDataType.pack(side="left", fill="both", padx=(10, 5))
    labelDataType.bind("<Button-1>", lambda event : show_message("info","* training data (X in the python script) :\nfile containing the measures of the features you want to train your model on.\n* training outcomes (y in the python script) :\nfile containing the ouctomes (the values you want to predict) corresponding to your training data.\n* validation data (X_test in the python script) :\nfile containing the measures of the features of which you want your model estimate the outcomes to evaluate its performances.\n* validation outcomes (y_test in the python script) :\nfile containing the ouctomes (the values you want to predict) corresponding to your validation data.\n* outer groups (groups in the python script) :\nfile containing information about the groups of samples you want to take into account when ou build your model.\n\nIf you are running a cross validation (cv) pipeline your data is either the training outcomes or training data.\nIf you are running one of the other pipelines your data can also be the validation outcomes or the validation data."))        
    
    # Specificity of the data
    subframeSpeChoice = CTkFrame(root, width=200, height=100)
    subframeSpeChoice.pack(side="top", fill="both", padx=10, pady=6)
    labelSpeChoice = CTkLabel(subframeSpeChoice, text="Type of data *")
    Speentry = CTkEntry(master=subframeSpeChoice, justify='center')
    
    def activate_spe(appear):
        if appear : 
            labelSpeChoice.pack(side="left", fill="both", padx=(10, 5))
            labelSpeChoice.bind("<Button-1>", lambda event : show_message("info","In the multi omic pipelines, we are using datasets \nof different natures (CyTOF, Proteomics, Metabolomics, ...)\nPlease specify the type of data that is in this file if you are using a multi omic pipeline."))        
            Speentry.pack(pady=6, padx=10, side='right')
        else:
            labelSpeChoice.pack_forget()
            Speentry.pack_forget()
    
    
    def switch_spe(event):
        if comboboxDataType.get() in ["training data", "validation data"]:
            activate_spe(True)
        else:
            activate_spe(False)
    
    comboboxDataType = CTkComboBox(subframeDataType, values=["training outcomes", "training data", "validation outcomes", "validation data", "outer groups"], width=300, command = switch_spe)
    comboboxDataType.pack(side="left", fill="both", padx=10, pady=5)
    
    def save_values_and_update_subframeDataDisplay():
        if len(Speentry.get()) > 0:
            file_list.set(file_list.get()+'\t'+comboboxDataType.get()+'\t'+Speentry.get()+'\n')
        else:
            file_list.set(file_list.get()+'\t'+comboboxDataType.get()+'\t'+' '+'\n')
        root.destroy()
        files = str(file_list.get()).split('\n')
        for widget in subframeName.winfo_children():
            widget.destroy()
        for widget in subframeType.winfo_children():
            widget.destroy()
        for widget in subframeSpe.winfo_children():
            widget.destroy()
        for file in files:
            display_file(subframeName, subframeType, subframeSpe, file)
    
    save_button = CTkButton(root, text="Save", command=save_values_and_update_subframeDataDisplay)
    save_button.pack(side="top", padx=10, pady=10)

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
        
def has_special_chars_or_spaces(input_string):
    pattern = re.compile('[^A-Za-z0-9]+') 
    return bool(pattern.search(input_string))
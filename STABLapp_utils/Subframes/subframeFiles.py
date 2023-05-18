#------------------------------------------------------------------------------------------------------------------------------
#
# Function : subframeFiles_display
#
# Description :
#       - arguments : root, foldername, file_list
#       - effect : Display three columns in which are going to added (and deleted) the name of the files that are imported in the
#                   project folder, the type of data contained in the folder and possible specification on the nature of the data
#                   (in case the stabl pipeline is a multi omic)
#
#------------------------------------------------------------------------------------------------------------------------------

from customtkinter import CTkButton, CTkLabel, CTkFrame, CTkScrollableFrame

from STABLapp_utils.SubframeComponents.Files.ImportFile import add_file_and_display_files
from STABLapp_utils.SubframeComponents.Files.DeleteFile import delete_file

def subframeFiles_display(root, foldername, file_list):
    label_frame = CTkFrame(root)
    label_frame.pack(side='top', fill='x', padx=10)
    labelDataDisplay = CTkLabel(master=label_frame, text="Imported data", font=("Roboto", 14, "bold")) 
    labelDataDisplay.pack(padx = 10, pady=3)
    
    subframeDataDisplay = CTkScrollableFrame(root)
    subframeDataDisplay.pack(side="top", fill='both', padx = 10, pady=6, expand=False)
    subframeName = CTkFrame(subframeDataDisplay)
    subframeName.pack(side="left", fill='both', padx = 10, pady=6, expand=True)
    labelName = CTkLabel(master=subframeName, text="File name", font=("Roboto", 12, "bold"))
    labelName.pack(padx = 10, pady=3)
    subframeType = CTkFrame(subframeDataDisplay)
    subframeType.pack(side="left", fill='both', padx = 10, pady=6, expand=True)
    labelType = CTkLabel(master=subframeType, text="Type of data", font=("Roboto", 12, "bold"))
    labelType.pack(padx = 10, pady=3)
    subframeSpe = CTkFrame(subframeDataDisplay)
    subframeSpe.pack(side="right", fill='both', padx = 10, pady=6, expand=True)
    labelSpe = CTkLabel(master=subframeSpe, text="Type of features", font=("Roboto", 12, "bold"))
    labelSpe.pack(padx = 10, pady=3)
    
    subframeButtons = CTkFrame(root, height=100, width=200)
    subframeButtons.pack(side="top", fill='both', padx = 10, pady=6)
    AddFileButton = CTkButton(subframeButtons, 
                              text="Import data file", 
                              command=lambda: add_file_and_display_files(foldername.get(), 
                                                                        file_list, 
                                                                        subframeName, subframeType, subframeSpe))
    AddFileButton.pack(side='left', padx=75, pady=6)
    AddFileButton = CTkButton(subframeButtons, 
                              text="Delete data file", 
                              command=lambda: delete_file(foldername.get(), 
                                                          file_list, 
                                                          subframeName, subframeType, subframeSpe))
    AddFileButton.pack(side='right', padx=75, pady=6)
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

from SubframeComponents.Files.ImportFile import add_file_and_display_files
from SubframeComponents.Files.DeleteFile import delete_file

def subframeFiles_display(root, foldername, file_list):
    label_frame = CTkFrame(root)
    label_frame.pack(side='top', fill='x', padx=10)
    labelDataDisplay = CTkLabel(master=label_frame, text="Imported data") 
    labelDataDisplay.pack(padx = 10, pady=3)
    
    subframeDataDisplay = CTkScrollableFrame(root)
    subframeDataDisplay.pack(side="top", fill='both', padx = 10, pady=6, expand=False)
    subframeName = CTkFrame(subframeDataDisplay)
    subframeName.pack(side="left", fill='both', padx = 10, pady=6, expand=True)
    subframeType = CTkFrame(subframeDataDisplay)
    subframeType.pack(side="left", fill='both', padx = 10, pady=6, expand=True)
    subframeSpe = CTkFrame(subframeDataDisplay)
    subframeSpe.pack(side="right", fill='both', padx = 10, pady=6, expand=True)
    
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
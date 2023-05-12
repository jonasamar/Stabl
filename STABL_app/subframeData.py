import customtkinter

from SubframeComponents.dataentry import data_entry

def subframeData_display(root, X_file, y_col, y_file):
    subframeData = customtkinter.CTkFrame(master=root)
    subframeData.pack(side="top", fill="both", pady=6, padx=10)
    
    labelPipeline = customtkinter.CTkLabel(subframeData, text="Data")
    labelPipeline.pack(pady=0, padx=10)
    
    data_entry(subframeData, X_file, y_col, y_file)
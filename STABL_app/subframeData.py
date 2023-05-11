import customtkinter

from subwindows import show_message

# Main frame
def subframeData_display(root, X_file, y_col, y_file):
    subframeData = customtkinter.CTkFrame(master=root)
    subframeData.pack(side="top", fill="both", pady=6, padx=10)
    
    labelPipeline = customtkinter.CTkLabel(subframeData, text="Data")
    labelPipeline.pack(pady=0, padx=10)
    
    data_entry(subframeData, X_file, y_col, y_file)
    
# Components
def data_entry(subframe1, X_file, y_col, y_file,):
    subframeX = customtkinter.CTkFrame(subframe1, width=200, height=100)
    subframeX.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
    subframeColY = customtkinter.CTkFrame(subframe1, width=200, height=100)
    subframeColY.pack(side="left", fill="both", expand=True, padx=5, pady=10)
    subframeY = customtkinter.CTkFrame(subframe1, width=200, height=100)
    subframeY.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)

    labelX = customtkinter.CTkLabel(subframeX, text="Datafile Name *")
    labelX.pack()
    labelX.bind("<Button-1>", lambda event : show_message("info", "The name you enter should correspond to the file with your entire dataset."))
    datafileX = customtkinter.CTkEntry(master=subframeX, textvariable = X_file, justify='center', placeholder_text="None")
    datafileX.pack(pady=6, padx=10)

    labelColY = customtkinter.CTkLabel(subframeColY, text="Outcome column *")
    labelColY.pack()
    labelColY.bind("<Button-1>", lambda event : show_message("info","If the file containing your entire dataset also contains the outcome you want to predict, you have to specify the name of the column corresponding to your outcome. Otherwise, leave this text box blank."))
    ColY = customtkinter.CTkEntry(master=subframeColY, textvariable=y_col, justify='center', placeholder_text="None")
    ColY.pack(pady=6, padx=10)

    labelY = customtkinter.CTkLabel(subframeY, text="Outcome file *")
    labelY.pack()
    labelY.bind("<Button-1>", lambda event : show_message("info","If you have a distinct file with the outcome you want to predict, enter the name of the file in this text box. Otherwise, leave this text box blank."))
    datafileY = customtkinter.CTkEntry(master=subframeY, textvariable=y_file, justify='center', placeholder_text="None")
    datafileY.pack(pady=6, padx=10)
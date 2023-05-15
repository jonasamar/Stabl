#------------------------------------------------------------------------------------------------------------------------------
#
# Function : stabl_fine_tuning
#
# Description :
#       - arguments : root
#       - effect : Open a new window in which the user can tune finer parameters
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter
    
def stabl_fine_tuning(root):
    subframeFineTuning = customtkinter.CTkFrame(root, width=200, height=100)
    subframeFineTuning.pack(side="top", fill="both",padx = 10, pady=6)
    FinerParamButton = customtkinter.CTkButton(master=subframeFineTuning, text="For even finer tuning...", command= lambda : fine_tuning_window())
    FinerParamButton.pack(side='top', padx = 10, pady=6)
    
def fine_tuning_window():
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("dark-blue")
    
    window = customtkinter.CTk()
    
    #TO DO...
    
    window.title('For even finer tuning...')
    label = customtkinter.CTkLabel(window, text='# TO DO !')
    label.pack(padx=20, pady=20)
    close_button = customtkinter.CTkButton(window, text="Close", command=window.destroy)
    close_button.pack(padx=20, pady=20)
    window.mainloop()
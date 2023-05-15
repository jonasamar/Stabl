#------------------------------------------------------------------------------------------------------------------------------
#
# Function : main()
#
# Description : Main window allowing users to chose one of the versions of the STABL App
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter

from STABLappv1 import app_v1
from STABLappv2 import app_v2

from subwindows.MessageWindow import show_message

def main():
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()
    root.geometry("400x150")
    root.title("STABL App")
    
    version = customtkinter.StringVar(value="v1")
    
    labelversion = customtkinter.CTkLabel(root, text="Chose the version of the STABL App you want :\n\t* 'v1' is the oldest\n\t* 'v2' is the most recent", justify='left')
    labelversion.pack(side="top", fill="both", padx=20, pady=20)
    
    subframeversion = customtkinter.CTkFrame(root, width=200, height=100)
    subframeversion.pack(pady=6, padx=10)
    labelversion = customtkinter.CTkLabel(subframeversion, text="STABL App version")
    labelversion.pack(side="left", fill="both", padx=(10, 5))
    comboboxversion = customtkinter.CTkComboBox(subframeversion, variable=version, values=["v1", "v2"], width=100)
    comboboxversion.pack(side="left", fill="both", padx=10, pady=5)
    
    def open_stabl_app(version):
        if version == 'v1':
            root.destroy()
            app_v1()
        elif version == 'v2':
            root.destroy()
            app_v2()
        else:
            show_message("Error", "This version of the Stabl App does not exist.")
            
    SelectVersion = customtkinter.CTkButton(master=subframeversion, text="Select", command= lambda : open_stabl_app(version.get()))
    SelectVersion.pack(side="top", padx=10, pady=5)

    root.mainloop()

main()
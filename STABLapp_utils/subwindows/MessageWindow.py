#------------------------------------------------------------------------------------------------------------------------------
#
# Function : show_message
#
# Description :
#       - arguments : type and message
#       - effect : Open a new window with a message and interrupt the script (thanks to the function mainloop).
#                   The message can be of different natures (type = 'Error' or 'info' or 'Warning' or others)
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter

def show_message(type, message):
    window = customtkinter.CTk()
    window.title(type)
    
    label = customtkinter.CTkLabel(window, justify='left', text=message)
    label.pack(padx=20, pady=20)
    
    close_button = customtkinter.CTkButton(window, text="Close", command=window.destroy)
    close_button.pack(padx=20, pady=20)

    
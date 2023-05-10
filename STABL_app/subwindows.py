import customtkinter

def show_message(type, message):
    """
    Create a window with a message which can be :
    - an Error message
    - an Info message
    - a Warning message
    """
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("dark-blue")
    
    window = customtkinter.CTk()
    
    window.title(type)
    label = customtkinter.CTkLabel(window, text=message)
    label.pack(padx=20, pady=20)
    close_button = customtkinter.CTkButton(window, text="Close", command=window.destroy)
    close_button.pack(padx=20, pady=20)
    window.mainloop()
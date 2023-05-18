import os
from customtkinter import CTk, CTkButton, filedialog

def delete_file(initialdir='./test'):
    file_path = filedialog.askopenfilename(initialdir=initialdir, title="Select file to delete")
    if file_path:
        try:
            os.remove(file_path)
            print("Success", f"File '{file_path}' deleted successfully.")
        except OSError as e:
            print("Error", f"Error deleting file '{file_path}': {e}")

root = CTk()
button = CTkButton(root, text="Delete File", command=delete_file)
button.pack()
root.mainloop()

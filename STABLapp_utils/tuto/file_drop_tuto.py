import os
import shutil
from customtkinter import CTk, CTkEntry, CTkButton, CTkLabel, filedialog


def select_file_and_copy_to_transfer_folder(transfer_folder):
    # Sélection du fichier source
    source_file_path = filedialog.askopenfilename(title="Select file")
    
    # Création du dossier de transfert s'il n'existe pas
    if not os.path.exists(transfer_folder):
        os.makedirs(transfer_folder)
    
    # Copie du fichier dans le dossier de transfert
    filename = os.path.basename(source_file_path)
    destination_file_path = os.path.join(transfer_folder, filename)
    shutil.copy(source_file_path, destination_file_path)
    
    # Affichage d'un message de confirmation
    CTkLabel(text="File copied to transfer folder").pack()


# Exemple d'utilisation
root = CTk()

# Champ de saisie de fichier
CTkEntry(root).pack()

# Bouton pour sélectionner le fichier et le copier dans le dossier de transfert
CTkButton(root, text="Copy to transfer folder", command=lambda: select_file_and_copy_to_transfer_folder("transfer")).pack()

root.mainloop()
#------------------------------------------------------------------------------------------------------------------------------
#
# Function : bootstrap_replace_tuning
#
# Description :
#       - arguments : subframeStabl, bootstrap_replace
#       - effect : Display a check box to activate or deactivate replacement in the bootstrap method of the Stabl model
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter

from subwindows.MessageWindow import show_message

def bootstrap_replace_tuning(subframeStabl, bootstrap_replace):
    subframeRepl = customtkinter.CTkFrame(subframeStabl, width=200, height=100)
    subframeRepl.pack(side="top", fill="both", padx=10, pady=6)

    labelrepl = customtkinter.CTkLabel(subframeRepl, text="Replace *")
    labelrepl.pack(side="left", fill="both", padx=(10, 5))
    labelrepl.bind("<Button-1>", lambda event : show_message("info","The way each bootstrap is built is by extracting a certain number or proportion of samples from your original dataset.\nThere are two ways of extracting those samples :\n\n\n\n\t* WITH replacement (Replace=True) : each time you select one sample from your original dataset to build your bootstrap, you replace it.\n\n\t(example : If you are doing a bootstrap of two cards within a deck of 52 cards with replacement, you would \n\t\t(1) pick a first card \n\t\t(2) pick a second card in another copy of your entire deck (you would still have 52 choices because you are picking a card from a brand new deck).\n\tConsequently you can pick twice the same card)\n\n\tThus, bootstraps with replacement can contain multiple copies of the same sample.\n\tThis kind of bootstrap becomes interesting when you have a low number of samples and a sample proportion close to 1. or greater than 1.\n\n\n\n\t* WITHOUT replacement (Replace=False) : each time you select one sample from your original dataset to build your bootstrap, you DON'T replace it.\n\n\t(example : If you are doing a bootstrap of two cards within a deck of 52 cards WITHOUT replacement, you would \n\t\t(1) pick a first card \n\t\t(2) pick a second card in the same deck (you would only have 51 choices because you already took one out).\n\tConsequently you CANNOT pick twice the same card)\n\n\tThus, bootstraps with replacement CANNOT contain multiple copies of the same sample.\n\tThis kind of bootstrap becomes interesting when you have a sample proportion close to 0.5"))

    checkboxrepl = customtkinter.CTkCheckBox(master=subframeRepl, variable=bootstrap_replace, text=None)
    checkboxrepl.pack(side="left", fill="both", padx=10, pady=5)
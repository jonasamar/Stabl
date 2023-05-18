#------------------------------------------------------------------------------------------------------------------------------
#
# Function : artificial_type_choice
#
# Description :
#       - arguments : subframeStabl, artificial_type
#       - effect : Display a combobox to chose the random method to generate the artificial features : random permutation or 
#                   knockoff.
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter

from STABLapp_utils.subwindows.MessageWindow import show_message

def artificial_type_choice(subframeStabl, artificial_type):
    subframeArti = customtkinter.CTkFrame(subframeStabl, width=200, height=100)
    subframeArti.pack(side="top", fill="both", padx=10, pady=6)
    
    labelarti = customtkinter.CTkLabel(subframeArti, text="Artificial type *")
    labelarti.pack(side="left", fill="both", padx=(10, 5))
    labelarti.bind("<Button-1>", lambda event : show_message("info","One of the first step in the STABL pipeline is to generate random features that we know are not interesting.\nThese features help STABL select the best FDR (false discovery rate) threshold possible (because they allow us to calculate a good estimate of the false discovery proportion : FDP+)).\n\nThe two strategies to generate these random features are random_permutation and knockoff. You can try both strategies and compare the results to see which one seems the most appropriate to your study."))
                   
    comboboxarti = customtkinter.CTkComboBox(subframeArti, variable=artificial_type, values=["random_permutation", "knockoff"], width=300)
    comboboxarti.pack(side="left", fill="both", padx=10, pady=5)
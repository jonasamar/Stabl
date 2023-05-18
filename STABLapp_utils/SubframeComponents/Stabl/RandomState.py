#------------------------------------------------------------------------------------------------------------------------------
#
# Function : random_state_tuning
#
# Description :
#       - arguments : subframeStabl, random_state
#       - effect : Display a scale to tune the the value of the random seed used in the Stabl model.
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter

from STABLapp_utils.subwindows.MessageWindow import show_message

def random_state_tuning(subframeStabl, random_state):
    subframeRand = customtkinter.CTkFrame(subframeStabl, width=200, height=100)
    subframeRand.pack(side="top", fill="both", padx=10, pady=6)
    
    labelval = customtkinter.CTkLabel(subframeRand, textvariable=random_state)
    labelval.pack()

    labelrand = customtkinter.CTkLabel(subframeRand, text="Random State *")
    labelrand.pack(side="left", fill="both", padx=(10, 5))
    labelrand.bind("<Button-1>", lambda event : show_message("info","Random state is the random seed used to initialize some values in the STABL pipeline.\nIt has to be an integer.\nIts value won't change drastically the performances of your model but you can try different values to take the best initialization possible for your model/ study."))

    randscale = customtkinter.CTkSlider(subframeRand, from_=0, to=100, orientation='horizontal', variable=random_state, number_of_steps=101, width=550)
    randscale.pack(side="left", fill="both", padx=10, pady=5)
#------------------------------------------------------------------------------------------------------------------------------
#
# Function : subframeStabl_display
#
# Description :
#       - arguments : root, paraemeters linked to the Stabl model the user wants to build
#       - effect : Display 
#                       - a slide to tune the l1 ratio of the elastic net model
#                       - a combobox for the artificial type the user wants to generate the artificial features
#                       - a slide to tune the sample fraction used in each bootstrap
#                       - a checkbox to activate or deactivate the replace mode of the bootstrapping method
#                       - a slide to chose the random state
#                       - a button to open a new window with some finer parameters to tune
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter

from STABLapp_utils.SubframeComponents.Stabl.l1Ratio import l1_ratio_tuning
from STABLapp_utils.SubframeComponents.Stabl.SampleFraction import sample_fraction_tuning
from STABLapp_utils.SubframeComponents.Stabl.ArtificialType import artificial_type_choice
from STABLapp_utils.SubframeComponents.Stabl.BootstrapReplace import bootstrap_replace_tuning
from STABLapp_utils.SubframeComponents.Stabl.RandomState import random_state_tuning
from STABLapp_utils.SubframeComponents.Stabl.StablFineTuning import stabl_fine_tuning

def subframeStabl_display(root, l1_ratio, artificial_type, sample_fraction, bootstrap_replace, random_state):
    # Main frame
    subframeStabl = customtkinter.CTkFrame(root, width=200, height=100)
    subframeStabl.pack(side="top", fill="both", padx=10, pady=6)
    labelStabl = customtkinter.CTkLabel(subframeStabl, text="Stabl model : parameter tuning", font=("Roboto", 14, "bold"))
    labelStabl.pack(pady=0, padx=10)
    
    # Subframes
    l1_ratio_tuning(subframeStabl, l1_ratio)
    artificial_type_choice(subframeStabl, artificial_type)
    sample_fraction_tuning(subframeStabl, sample_fraction)
    bootstrap_replace_tuning(subframeStabl, bootstrap_replace)
    random_state_tuning(subframeStabl, random_state)
    stabl_fine_tuning(root)
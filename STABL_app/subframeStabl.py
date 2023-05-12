import customtkinter

from SubframeComponents.l1ratio import l1_ratio_tuning
from SubframeComponents.samplefraction import sample_fraction_tuning
from SubframeComponents.artificialtype import artificial_type_choice
from SubframeComponents.replace import replace_tuning
from SubframeComponents.randomstate import random_state_tuning
from SubframeComponents.stablfinetuning import stabl_fine_tuning

def subframeStabl_display(root, ratioval, artificial_type, sample_fraction, replace, random_state):
    subframeStabl = customtkinter.CTkFrame(root, width=200, height=100)
    subframeStabl.pack(side="top", fill="both", padx=10, pady=6)
    
    labelStabl = customtkinter.CTkLabel(subframeStabl, text="Stabl : fine tuning")
    labelStabl.pack(pady=0, padx=10)
    
    l1_ratio_tuning(subframeStabl, ratioval)
    artificial_type_choice(subframeStabl, artificial_type)
    sample_fraction_tuning(subframeStabl, sample_fraction)
    replace_tuning(subframeStabl, replace)
    random_state_tuning(subframeStabl, random_state)
    stabl_fine_tuning(root)
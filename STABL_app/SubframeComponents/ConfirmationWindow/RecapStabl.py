#------------------------------------------------------------------------------------------------------------------------------
#
# Function : recap_stabl_params
#
# Description :
#       - arguments : parameters linked to the Stabl model
#       - effect : Display the parameters of the Stabl model selected by the user
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter
import pandas as pd

def recap_stabl_params(root, l1_ratio, artificial_type, sample_fraction, bootstrap_replace, random_state):
    
    labelStabl = customtkinter.CTkLabel(root, justify='center', text='Stabl model parameters', font=('Roboto', 14))
    labelStabl.pack()  
    SubframeStabl = customtkinter.CTkFrame(root)
    SubframeStabl.pack(side='top', fill='both', padx=10, pady=6)
       
    labelRatio = customtkinter.CTkLabel(SubframeStabl, text='L1/L2 ratio : '+str(l1_ratio.get()), justify='left')
    labelRatio.pack(side='top', padx=10, pady=6, anchor="w")
    
    labelArti = customtkinter.CTkLabel(SubframeStabl, text='Artificial type : '+artificial_type.get(), justify='left')
    labelArti.pack(side='top', padx=10, pady=6, anchor="w")
    
    labelSampleFrac = customtkinter.CTkLabel(SubframeStabl, text='Bootstrap sample fraction : '+str(sample_fraction.get()), justify='left')
    labelSampleFrac.pack(side='top', padx=10, pady=6, anchor="w")
    
    if bootstrap_replace.get():
        status = 'Activated'
    else:
        status = 'Deactivated'
        
    labelReplace = customtkinter.CTkLabel(SubframeStabl, text='Replacement (for bootstrapping) : '+status, justify='left')
    labelReplace.pack(side='top', padx=10, pady=6, anchor="w")
    
    labelRdState = customtkinter.CTkLabel(SubframeStabl, text='Random state : '+str(random_state.get()), justify='left')
    labelRdState.pack(side='top', padx=10, pady=6, anchor="w")
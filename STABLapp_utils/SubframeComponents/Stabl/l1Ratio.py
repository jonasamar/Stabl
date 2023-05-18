#------------------------------------------------------------------------------------------------------------------------------
#
# Function : l1_ratio_tuning
#
# Description :
#       - arguments : subframeStabl, l1_ratio
#       - effect : Display a scale to tune the l1 ratio of the elastic net model Stabl is going to be built on.
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter

from STABLapp_utils.subwindows.MessageWindow import show_message

def l1_ratio_tuning(subframeStabl, l1_ratio):
    subframeRatio = customtkinter.CTkFrame(subframeStabl, width=200, height=100)
    subframeRatio.pack(side="top", fill="both", padx=10, pady=6)
    
    l1_ratio_display = customtkinter.StringVar(value="ElasticNet 1.")
    labelval = customtkinter.CTkLabel(subframeRatio, textvariable=l1_ratio_display)
    labelval.pack()

    labelratio = customtkinter.CTkLabel(subframeRatio, text="L1/L2 Ratio *")
    labelratio.pack(side="left", fill="both", padx=(10, 5))
    labelratio.bind("<Button-1>", lambda event : show_message("info","This ratio correspond to how sparse you want your model.\n\n\t* If the ratio = 1., a l1 penalty is applied (lasso model) which will give the sparsest model. \n\n\t* If the ratio = 0., a l2 penalty is applied (ridge regression model) corresponding to the least sparse model.\n\nThe values in between correspond to models whose sparsity are between these extrem models."))
    
    labelridge = customtkinter.CTkLabel(subframeRatio, text="(L2) Ridge\nRegression", font=("Roboto", 10))
    labelridge.pack(side="left", padx=(10, 6))

    def update_ratio_display(event):
        l1_ratio_display.set(f"ElasticNet {l1_ratio.get()}")
        
    ratioscale = customtkinter.CTkSlider(subframeRatio, from_=0., to=1., orientation='horizontal', variable=l1_ratio, height=18, number_of_steps=50, command=update_ratio_display)
    ratioscale.pack(side="left", fill="x", padx=10, pady=5, expand=True)
    
    labelLasso = customtkinter.CTkLabel(subframeRatio, text="(L1)\nLASSO", font=("Roboto", 10))
    labelLasso.pack(side="right", padx=(10, 6))
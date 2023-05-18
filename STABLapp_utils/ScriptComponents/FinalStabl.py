#------------------------------------------------------------------------------------------------------------------------------
#
# Function : final_stabl
#
# Description :
#       - arguments : fpy (python file), preprocess (Bool), stabl_pipeline, task_type
#       - effect : Add lines of code to the python script to build a final Stabl model and get the results of this model
#
#------------------------------------------------------------------------------------------------------------------------------

def final_stabl(fpy, foldername, preprocess, stabl_pipeline, task_type):
    if stabl_pipeline == 'single_omic_stabl_cv': 
        fpy.write("\n")
        fpy.write("#Final STABL\n")
        fpy.write("finalstabl = clone(stabl)\n")
        if preprocess:
            fpy.write("finalstabl.fit(X_STD,y.astype(int))\n")
            fpy.write("\n")
            fpy.write(f"save_stabl_results(finalstabl,'../{foldername}/Results'+'/FinalSTABL/',X_STD,y,task_type='{task_type}')\n")
        else: 
            fpy.write("finalstabl.fit(X, y.astype(int))\n")
            fpy.write("\n")
            fpy.write(f"save_stabl_results(finalstabl,'../{foldername}/Results'+'/FinalSTABL/',X,y,task_type='{task_type}')\n")
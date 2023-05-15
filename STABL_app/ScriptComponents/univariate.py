#------------------------------------------------------------------------------------------------------------------------------
#
# Function : univariate_analysis
#
# Description :
#       - arguments : fpy (python file), task_type, stabl_pipeline
#       - effect : Add lines of code to the python script so that the python script create a Univariate folder in the Result 
#                   folder containing the univariate analysis of the most interesting features (the univariate analysis depends
#                   on the nature of the task : 'binary' or 'regression')
#
#------------------------------------------------------------------------------------------------------------------------------

def univariate_analysis(fpy, foldername, task_type, stabl_pipeline):
    if task_type == 'binary':
        testname = "mannwhitneyu"
        plot= "boxplot"        
        save = 'Mann-WhitneyU-test'
    else: # task_type = regression
        testname = "pearsonr"
        plot= "scatterplot"
        save = 'Pearsonr'
    fpy.write("\n")
    fpy.write("#Univariate\n")
    fpy.write("os.makedirs('./{foldername}/Results/Univariate', exist_ok=True)\n")
    if 'single' in stabl_pipeline:
        fpy.write("vals1 = []\n")
        fpy.write("vals2 = []\n")
        fpy.write("for col in X.columns:\n")
        fpy.write(f"\ta,b = {testname}(X.loc[y == 0,col].to_numpy(),X.loc[y == 1,col].to_numpy())\n")
        fpy.write("\tvals1.append(a)\n")
        fpy.write("\tvals2.append(b)\n")
        fpy.write("\n")
        fpy.write(f"res = pd.DataFrame(data=[vals1,vals2],index= ['{save}','p-value'],columns=X.columns)\n")
        fpy.write("res = res.sort_values(by='p-value',axis=1)\n")
        fpy.write(f"res.T.to_csv('./{foldername}/Results/Univariate/' + '{save}Pval.csv')\n")
        fpy.write("\n")
        fpy.write(f"{plot}_features(\n\tlist_of_features=res.columns[:10],\n\tdf_X=X[res.columns[:10]],\n\ty=y,\n\tshow_fig=False,\n\texport_file=True,\n\tpath ='./{foldername}/Results/Univariate'\n)\n")
    elif 'multi' in stabl_pipeline:
        fpy.write("for omic in train_data_dict.keys():\n")
        fpy.write("\tos.makedirs('./{foldername}/Results/Univariate/'+omic, exist_ok=True)\n")
        fpy.write("\tX = train_data_dict[omic]\n")
        fpy.write("\tvals1 = []\n")
        fpy.write("\tvals2 = []\n")
        fpy.write("\tfor col in X.columns:\n")
        fpy.write(f"\t\ta,b = {testname}(X.loc[y == 0,col].to_numpy(),X.loc[y == 1,col].to_numpy())\n")
        fpy.write("\t\tvals1.append(a)\n")
        fpy.write("\t\tvals2.append(b)\n")
        fpy.write("\n")
        fpy.write(f"\tres = pd.DataFrame(data=[vals1,vals2],index= ['{save}','p-value'],columns=X.columns)\n")
        fpy.write("\tres = res.sort_values(by='p-value',axis=1)\n")
        fpy.write(f"\tres.T.to_csv('./{foldername}/Results/Univariate/'+omic+'/' + '{save}Pval.csv')\n")
        fpy.write("\n")
        fpy.write(f"\t{plot}_features(\n\tlist_of_features=res.columns[:10],\n\tdf_X=X[res.columns[:10]],\n\ty=y,\n\tshow_fig=False,\n\texport_file=True,\n\tpath ='./{foldername}/Results/Univariate/'+omic\n\t)\n")
   
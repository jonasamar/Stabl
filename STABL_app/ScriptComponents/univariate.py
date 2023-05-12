def univariate_analysis(fpy, task_type):
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
    fpy.write("os.makedirs('./Results/Univariate', exist_ok=True)\n")
    fpy.write("vals1 = []\n")
    fpy.write("vals2 = []\n")
    fpy.write("for col in X.columns:\n")
    fpy.write(f"\ta,b = {testname}(X.loc[y == 0,col].to_numpy(),X.loc[y == 1,col].to_numpy())\n")
    fpy.write("\tvals1.append(a)\n")
    fpy.write("\tvals2.append(b)\n")
    fpy.write("\n")
    fpy.write(f"res = pd.DataFrame(data=[vals1,vals2],index= ['{save}','p-value'],columns=X.columns)\n")
    fpy.write("res = res.sort_values(by='p-value',axis=1)\n")
    fpy.write(f"res.T.to_csv('./Results/Univariate/' + '{save}Pval.csv')\n")
    fpy.write("\n")
    fpy.write(f"{plot}_features(\n\tlist_of_features=res.columns[:10],\n\tdf_X=X[res.columns[:10]],\n\ty=y,\n\tshow_fig=False,\n\texport_file=True,\n\tpath ='./Results/Univariate'\n)\n")

def final_stabl(fpy, preprocess):
    fpy.write("\n")
    fpy.write("#Final STABL\n")
    fpy.write("finalstabl = clone(stabl)\n")
    if preprocess:
        fpy.write("finalstabl.fit(X_STD,y.astype(int))\n")
        fpy.write("\n")
        fpy.write("save_stabl_results(finalstabl,'./Results'+'/FinalSTABL/',X_STD,y,task_type='binary')\n")
    else: 
        fpy.write("finalstabl.fit(X, y.astype(int))\n")
        fpy.write("\n")
        fpy.write("save_stabl_results(finalstabl,'./Results'+'/FinalSTABL/',X,y,task_type='binary')\n")
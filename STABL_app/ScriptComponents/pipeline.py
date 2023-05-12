from subwindows import show_message

def pipeline(fpy, stabl_pipeline, task_type, outer_groups, X_test, y_test_col, y_test):
    fpy.write("\n")
    if stabl_pipeline in ["multi_omic_stabl_cv",  "single_omic_stabl_cv"]:
        fpy.write(f"{stabl_pipeline}(\n\tX=X,\n\ty=y.astype(int),\n\touter_splitter=outer_splitter,\n\tstabl=stabl,\n\tstability_selection=stability_selection,\n\ttask_type='{task_type}',\n\tsave_path='./Results'")
        if len(outer_groups) > 0:
            fpy.write(f",\n\touter_groups='{outer_groups}')\n")
        else:
            fpy.write(f"\n)\n")

    elif stabl_pipeline in ["multi_omic_stabl",  "single_omic_stabl"]:
        if len(X_test) > 0:
            fpy.write("#Import Validation Data\n")
            fpy.write(f"X_test = pd.read_csv('./{X_test}',index_col=0)\n")
            if (y_test != "") and (y_test_col == ""):
                fpy.write(f"y_test = pd.read_csv('./{y_test}',index_col=0).iloc[:,0]\n")
                fpy.write("\n")
            elif (y_test == "") and (y_test_col != ""):
                fpy.write(f"y_test = X_test[{y_test_col}]\n")
                fpy.write(f"X_test.drop({y_test_col}, axis=1, inplace=True)\n")
                fpy.write("\n")
            elif (y_test != "") and (y_test_col != ""):
                fpy.write(f"y_test = pd.read_csv('./{y_test}',index_col=0).iloc[:,0]\n")
                fpy.write(f"X_test.drop('{y_test_col}', axis=1, inplace=True)\n")
                fpy.write("\n")
            else :
                fpy.write(f"y_test = #MISSING INFORMATION")
                show_message("Error", "Cannot import your validation data because we don't know where your outcomes are. You need to fill at least one of the two text boxes ('Outome column' or 'Outcome file')")
            fpy.write(f"{stabl_pipeline}(\n\tX=X,\n\ty=y.astype(int),\n\touter_splitter=outer_splitter,\n\tstabl=stabl,\n\tstability_selection=stability_selection,\n\ttask_type='{task_type}',\n\tsave_path='./Results',\n\t")
            fpy.write(f"X_test=X_test,\n\ty_test=y_test)\n")
        else:
            fpy.write(f"{stabl_pipeline}(\n\tX=X,\n\ty=y.astype(int),\n\touter_splitter=outer_splitter,\n\tstabl=stabl,\n\tstability_selection=stability_selection,\n\ttask_type='{task_type}',\n\tsave_path='./Results')\n")
    else:
        show_message("Error", "The pipeline you have chosen is not recognized.\nPlease chose one of the pipelines suggested in the pipeline combobox.")


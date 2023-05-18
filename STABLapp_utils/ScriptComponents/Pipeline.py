#------------------------------------------------------------------------------------------------------------------------------
#
# Function : pipeline
#
# Description :
#       - arguments : all the parameters selected by the user regarding the choice of Stabl pipeline.
#       - effect : Add lines of code to the python script to call the desired Stabl pipeline and put the desired argument values 
#
#------------------------------------------------------------------------------------------------------------------------------

from STABLapp_utils.subwindows.MessageWindow import show_message

def pipeline(version,
             fpy,
             foldername,
             stabl_pipeline, 
             task_type, 
             outer_groups, 
             X_test, y_test_col, y_test):

    if not '_cv' in stabl_pipeline:
        if len(X_test) > 0:
            fpy.write("\n") 
            fpy.write("#Import Validation Data\n")
            if version == 'v1':
                fpy.write(f"X_test = pd.read_csv('../{foldername}/{X_test}',index_col=0)\n")
                if (y_test != "") and (y_test_col == ""):
                    fpy.write(f"y_test = pd.read_csv('../{foldername}/{y_test}',index_col=0).iloc[:,0]\n")
                    fpy.write("\n")
                elif (y_test == "") and (y_test_col != ""):
                    fpy.write(f"y_test = X_test[{y_test_col}]\n")
                    fpy.write(f"X_test.drop({y_test_col}, axis=1, inplace=True)\n")
                    fpy.write("\n")
                elif (y_test != "") and (y_test_col != ""):
                    fpy.write(f"y_test = pd.read_csv('../{foldername}/{y_test}',index_col=0).iloc[:,0]\n")
                    fpy.write(f"X_test.drop('{y_test_col}', axis=1, inplace=True)\n")
                    fpy.write("\n")
                else :
                    fpy.write(f"y_test = #MISSING INFORMATION")
                    show_message("Error", "Cannot import your validation data because we don't know where your outcomes are. You need to fill at least one of the two text boxes ('Outome column' or 'Outcome file')")
            elif version == 'v2':
                X_files = X_test.split('\n')
                y_files = y_test.split('\n')
                y = y_files[1].split('\t')[0]
                if 'single' in stabl_pipeline:
                    X = X_files[1].split('\t')[0]
                    fpy.write(f"X_test = pd.read_csv('../{foldername}/{X}',index_col=0)\n")
                    
                if 'multi' in stabl_pipeline:
                    file_dict = {}
                    for file in X_files:
                        if len(file) > 0:
                            name, spe = file.split('\t')[0], file.split('\t')[1]
                            file_dict[spe] = name
                    fpy.write("X_test = {\n")
                    for i, el in enumerate(file_dict.keys()):
                        if i < len(file_dict.keys()) - 1:
                            fpy.write(f"\t'{el}': pd.read_csv('../{foldername}/{file_dict[el]}',index_col=0),\n")
                        else:
                            fpy.write(f"\t'{el}': pd.read_csv('../{foldername}/{file_dict[el]}',index_col=0)\n")
                    fpy.write("}")
                fpy.write("\n") 
                fpy.write(f"y_test = pd.read_csv('../{foldername}/{y}',index_col=0).iloc[:,0]\n")
          
    fpy.write("\n")        
    if 'multi' in stabl_pipeline:
        fpy.write(f"{stabl_pipeline}(\n\ttrain_data_dict,\n\ty.astype(int),\n\t")
    elif 'single' in stabl_pipeline:
        fpy.write(f"{stabl_pipeline}(\n\tX=X,\n\ty=y.astype(int),\n\t")
    
    fpy.write(f"outer_splitter=outer_splitter,\n\tstabl=stabl,\n\tstability_selection=stability_selection,\n\ttask_type='{task_type}',\n\tsave_path='../{foldername}/Results'")

    if '_cv' in stabl_pipeline:
        if len(outer_groups) > 0:
            fpy.write(f",\n\touter_groups='{outer_groups}')\n")
        else:
            fpy.write(f"\n)\n")
    elif '_cv' not in stabl_pipeline:
        if len(X_test) > 0:
            fpy.write(f",\n\tX_test=X_test,\n\ty_test=y_test)\n")
        else:
            fpy.write(f"\n)\n")
            
            
        
#------------------------------------------------------------------------------------------------------------------------------
#
# Function : import_data
#
# Description :
#       - arguments : fpy (python file), X_file, y_col, y_file
#       - effect : Add lines of code to the python script to import the data on which the user want to run STABL
#
#------------------------------------------------------------------------------------------------------------------------------

from subwindows.MessageWindow import show_message

def import_data(version, fpy, foldername, X_file, y_col, y_file, stabl_pipeline):

    fpy.write("#Import Data\n")
    if version == 'v1':
        fpy.write(f"X = pd.read_csv('./{foldername}/{X_file}',index_col=0)\n")
        if (y_file != "") and (y_col == ""):
            fpy.write(f"y = pd.read_csv('./{foldername}/{y_file}',index_col=0).iloc[:,0]\n")
            fpy.write("\n")
        elif (y_file == "") and (y_col != ""):
            fpy.write(f"y = X[{y_col}]\n")
            fpy.write(f"X.drop({y_col}, axis=1, inplace=True)\n")
            fpy.write("\n")
        elif (y_file != "") and (y_col != ""):
            fpy.write(f"y = pd.read_csv('./{foldername}/{y_file}',index_col=0).iloc[:,0]\n")
            fpy.write(f"X.drop('{y_col}', axis=1, inplace=True)\n")
            fpy.write("\n")
        else :
            show_message("Error", "Cannot import your data because we don't know where your outcomes are. You need to fill at least one of the two text boxes ('Outome column' or 'Outcome file')")
    
    elif version =='v2':
        X_files = X_file.split('\n')
        y_files = y_file.split('\n')
        y = y_files[1].split('\t')[0]
        if 'single' in stabl_pipeline:
            X = X_files[1].split('\t')[0]
            fpy.write(f"X = pd.read_csv('./{foldername}/{X}',index_col=0)\n")
            
        if 'multi' in stabl_pipeline:
            file_dict = {}
            for file in X_files:
                if len(file) > 0:
                    name, spe = file.split('\t')[0], file.split('\t')[1]
                    file_dict[spe] = name
            fpy.write("train_data_dict = {\n")
            for i, el in enumerate(file_dict.keys()):
                if i < len(file_dict.keys()) - 1:
                    fpy.write(f"\t'{el}': pd.read_csv('./{foldername}/{file_dict[el]}',index_col=0),\n")
                else:
                    fpy.write(f"\t'{el}': pd.read_csv('./{foldername}/{file_dict[el]}',index_col=0)\n")
            fpy.write("}")
        fpy.write("\n") 
        fpy.write(f"y = pd.read_csv('./{foldername}/{y}',index_col=0).iloc[:,0]\n")
        fpy.write("\n") 

from subwindows import show_message

def import_data(fpy, X_file, y_col, y_file):
    fpy.write("#Import Data\n")
    fpy.write(f"X = pd.read_csv('./{X_file}',index_col=0)\n")
    if (y_file != "") and (y_col == ""):
        fpy.write(f"y = pd.read_csv('./{y_file}',index_col=0).iloc[:,0]\n")
        fpy.write("\n")
    elif (y_file == "") and (y_col != ""):
        fpy.write(f"y = X[{y_col}]\n")
        fpy.write(f"X.drop({y_col}, axis=1, inplace=True)\n")
        fpy.write("\n")
    elif (y_file != "") and (y_col != ""):
        fpy.write(f"y = pd.read_csv('./{y_file}',index_col=0).iloc[:,0]\n")
        fpy.write(f"X.drop('{y_col}', axis=1, inplace=True)\n")
        fpy.write("\n")
    else :
        show_message("Error", "Cannot import your data because we don't know where your outcomes are. You need to fill at least one of the two text boxes ('Outome column' or 'Outcome file')")
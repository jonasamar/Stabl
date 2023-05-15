#------------------------------------------------------------------------------------------------------------------------------
#
# Function : recap_files_and_var_reorganization
#
# Description :
#       - arguments : root, file related variables
#       - effect : Display the names of the data files which have been imported ordered by categories (training data/ training 
#                   outcome/ validation data/ validation outcome/ outer groups)
#                  Reorganize the variables by putting into X_file and y_file the values of file_list to train the model and in
#                   X_test and y_test the files to validate the model (and outer  groups if there are outer groups)
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter
import pandas as pd

def recap_files_and_var_reorganization(root, 
                                       file_list, 
                                       X_file, y_file, 
                                       X_test, y_test, 
                                       outer_groups):
    
    labelData = customtkinter.CTkLabel(root, justify='center', text='Data Imported', font=('Roboto', 14))
    labelData.pack()
    SubframeData = customtkinter.CTkScrollableFrame(root)
    SubframeData.pack(side='top', fill='both', padx=10, pady=6)
    
    files = (file_list.get()).split('\n')
    dict_files = {}
    for file in files:
        if len(file) > 0:
            elements = file.split('\t')
            name, datatype, spe = elements[0], elements[2], elements[3]
            dict_files[name] = {'type': datatype, 'spe':spe}
    df = pd.DataFrame(dict_files, index=['type', 'spe']).T            
    
    ## Train Data
    labelTrainData = customtkinter.CTkLabel(SubframeData, justify='center', text='Training Data', font=('Roboto', 12, "bold"))
    labelTrainData.pack(padx=10, pady=6)
    data_display_and_organization(SubframeData, df, 'training data', X_file)
    ## Train Ouctomes
    labelTrainOut = customtkinter.CTkLabel(SubframeData, justify='center', text='Training Ouctome', font=('Roboto', 12, "bold"))
    labelTrainOut.pack(padx=10, pady=6)
    data_display_and_organization(SubframeData, df, 'training outcomes', y_file)
    ## Validation Data
    labelValData = customtkinter.CTkLabel(SubframeData, justify='center', text='Validation Data', font=('Roboto', 12, "bold"))
    labelValData.pack(padx=10, pady=6)
    data_display_and_organization(SubframeData, df, 'validation data', X_test)
    ## Train Ouctomes
    labelValOut = customtkinter.CTkLabel(SubframeData, justify='center', text='Validation Ouctome', font=('Roboto', 12, "bold"))
    labelValOut.pack(padx=10, pady=6)
    data_display_and_organization(SubframeData, df,'validation outcomes', y_test)
    ## Train Ouctomes
    labelGroup = customtkinter.CTkLabel(SubframeData, justify='center', text='Groups', font=('Roboto', 12, "bold"))
    labelGroup.pack(padx=10, pady=6)
    data_display_and_organization(SubframeData, df, 'outer groups', outer_groups)

def data_display_and_organization(root, df, datatype, var):
    filenames = df[df['type']==datatype].index
    var.set('')
    if len(filenames) > 0:
        for filename in filenames:
            Subframe = customtkinter.CTkFrame(root)
            Subframe.pack(side='top', fill='both', padx=10, pady=6)
            labelname = customtkinter.CTkLabel(Subframe, justify='center', text=filename)
            labelname.pack(side='left', padx=10, pady=6)
            labelspe = customtkinter.CTkLabel(Subframe, justify='center', text=df.loc[filename, 'spe'])
            labelspe.pack(side='right', padx=10, pady=6)
            var.set(var.get()+'\n'+filename+'\t'+df.loc[filename, 'spe'])
    else:
        Subframe = customtkinter.CTkFrame(root)
        Subframe.pack(side='top', fill='both', padx=10, pady=6)
        label = customtkinter.CTkLabel(Subframe, justify='center', text='Empty')
        label.pack(side='top')
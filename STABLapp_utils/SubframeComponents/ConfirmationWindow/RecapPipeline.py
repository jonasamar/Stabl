#------------------------------------------------------------------------------------------------------------------------------
#
# Function : recap_files_and_var_reorganization
#
# Description :
#       - arguments : parameters linked to choice of the pipeline
#       - effect : Display the information of the pipeline selected by the user
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter

def recap_pipeline_params(root, preprocess, outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size, pipeline, task_type):
    
    labelPip = customtkinter.CTkLabel(root, justify='center', text='Choice of pipeline', font=('Roboto', 14))
    labelPip.pack()  
    SubframePip = customtkinter.CTkFrame(root)
    SubframePip.pack(side='top', fill='both', padx=10, pady=6)
       
    if preprocess.get():
        status = 'Activated'
    else:
        status = 'Deactivated'
    labelPreprocess = customtkinter.CTkLabel(SubframePip, text='Preprocessing : '+status, justify='left')
    labelPreprocess.pack(side='top', padx=10, pady=6, anchor="w")
    
    pipeline_name = ""
    if pipeline.get()=="multi_omic_stabl":
        pipeline_name = "Multi-omic Validation"
    if pipeline.get()=="multi_omic_stabl_cv":
        pipeline_name = "Multi-omic Training"
    if pipeline.get()=="single_omic_stabl":
        pipeline_name = "Single-omic Validation"
    if pipeline.get()=="single_omic_stabl_cv":
        pipeline_name = "Single-omic Training"

    labelPipeline = customtkinter.CTkLabel(SubframePip, text='Pipeline : '+pipeline_name, justify='left')
    labelPipeline.pack(side='top', padx=10, pady=6, anchor="w")
    
    labelTaskType = customtkinter.CTkLabel(SubframePip, text='Task type : '+task_type.get(), justify='left')
    labelTaskType.pack(side='top', padx=10, pady=6, anchor="w")
    
    labelOutSplit = customtkinter.CTkLabel(SubframePip, text='Outer splitter : '+outersplitter.get(), justify='left')
    labelOutSplit.pack(side='top', padx=10, pady=6, anchor="w")
    
    if outersplitter.get() == 'RepeatedStratifiedKFold':
        labelNsplits = customtkinter.CTkLabel(SubframePip, text='\t * n_splits : '+str(n_splits.get()), justify='left')
        labelNsplits.pack(side='top', padx=10, pady=6, anchor="w")
        labelNrepeat = customtkinter.CTkLabel(SubframePip, text='\t * n_repeats : '+str(n_repeat.get()), justify='left')
        labelNrepeat.pack(side='top', padx=10, pady=6, anchor="w")
        labelRdState = customtkinter.CTkLabel(SubframePip, text='\t * random_state : '+str(cv_rd.get()), justify='left')
        labelRdState.pack(side='top', padx=10, pady=6, anchor="w")
        
    elif outersplitter.get() == 'GroupShuffleSplit':
        labelNsplits = customtkinter.CTkLabel(SubframePip, text='\t * n_splits : '+str(n_splits.get()), justify='left')
        labelNsplits.pack(side='top', padx=10, pady=6, anchor="w")
        labelTestSize = customtkinter.CTkLabel(SubframePip, text='\t * test_size : '+str(test_size.get()), justify='left')
        labelTestSize.pack(side='top', padx=10, pady=6, anchor="w")
        labelTrainSize = customtkinter.CTkLabel(SubframePip, text='\t * train_size : '+str(train_size.get()), justify='left')
        labelTrainSize.pack(side='top', padx=10, pady=6, anchor="w")
        labelRdState = customtkinter.CTkLabel(SubframePip, text='\t * random_state : '+str(cv_rd.get()), justify='left')
        labelRdState.pack(side='top', padx=10, pady=6, anchor="w")
    
    
    
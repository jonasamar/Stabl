#------------------------------------------------------------------------------------------------------------------------------
#
# Function : subframePipeline_display
#
# Description :
#       - arguments : version (of the app), root, paraemeters linked to the choice of pipeline the user wants to run
#       - effect : Display 
#                       - a combobox to chose one of the pipelines
#                       - a combobox to chose the type of task (binary or regression)
#                       - a checkbox to activate or deactivate preprocessing
#                       - a button opening a new window with other possible parameters to tune
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter

from STABLapp_utils.SubframeComponents.Pipeline.Preprocessing import preprocess_activation
from STABLapp_utils.SubframeComponents.Pipeline.PipelineChoice import pipeline_choice
from STABLapp_utils.SubframeComponents.Pipeline.TaskType import task_type_display
from STABLapp_utils.SubframeComponents.Pipeline.PipelineFineTuning import pipeline_fine_tuning

def subframePipeline_display(version, 
                             root, 
                             preprocess, 
                             outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size, 
                             pipeline, 
                             task_type, 
                             outer_groups=None, 
                             X_test=None, y_test_col=None, y_test=None):
    # Main frame
    subframePipeline = customtkinter.CTkFrame(root, width=200, height=100)
    subframePipeline.pack(side="top", fill="both", padx=10, pady=6)
    labelPipeline = customtkinter.CTkLabel(subframePipeline, text="Pipeline and parameters", font=("Roboto", 14, "bold"))
    labelPipeline.pack(pady=0, padx=10)

    # Subframes
    task_type_display(subframePipeline, task_type)
    preprocess_activation(version, subframePipeline, preprocess)
    pipeline_choice(version, subframePipeline, pipeline, outer_groups, X_test, y_test_col, y_test, outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size)
    pipeline_fine_tuning(root)
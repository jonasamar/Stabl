import customtkinter

from SubframeComponents.preprocessing import preprocess_activation
from SubframeComponents.outersplitter import outer_splitter_tuning
from SubframeComponents.pipelinechoice import pipeline_choice
from SubframeComponents.pipelinefinetuning import pipeline_fine_tuning

# Main frame
def subframePipeline_display(root, preprocess, outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size, pipeline, task_type, outer_groups, X_test, y_test_col, y_test):
    subframePipeline = customtkinter.CTkFrame(root, width=200, height=100)
    subframePipeline.pack(side="top", fill="both", padx=10, pady=6)
    
    labelPipeline = customtkinter.CTkLabel(subframePipeline, text="Pipeline and parameters")
    labelPipeline.pack(pady=0, padx=10)

    preprocess_activation(subframePipeline, preprocess)
    outer_splitter_tuning(subframePipeline, outersplitter, n_splits, n_repeat, cv_rd, test_size, train_size)
    pipeline_choice(root, subframePipeline, pipeline, task_type, outer_groups, X_test, y_test_col, y_test)
    pipeline_fine_tuning(root)
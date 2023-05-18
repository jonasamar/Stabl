#------------------------------------------------------------------------------------------------------------------------------
#
# Function : subframeSbatch_display
#
# Description :
#       - arguments : root, paraemeters linked to the job the user want to send to sherlock
#       - effect : Display 
#                       - time textboxes to enter a time limit to the job the user wants to run
#                       - a combobox for the number of CPUs the user wants to assign to the job
#                       - a combobox for the memory per CPU the user wants to assign to the job
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter

from STABLapp_utils.subwindows.MessageWindow import show_message

from STABLapp_utils.SubframeComponents.Sbatch.TimeLimit import time_limit
from STABLapp_utils.SubframeComponents.Sbatch.CPUparams import cpu_params
from STABLapp_utils.SubframeComponents.Sbatch.SbatchFineTuning import sbatch_fine_tuning

def subframeSbatch_display(root, days, hours, minutes, sec, nb_cpu, mem_cpu):
    labelSbatch = customtkinter.CTkLabel(root, text="Sbatch file parameters *", font=("Roboto", 16, 'bold'))
    labelSbatch.pack(pady=15, padx=15)
    labelSbatch.bind("<Button-1>", lambda event : show_message("info", "In order to run your python script on Sherlock,\nyou need to create a.sbatch file.\nMost parameters can be left by default,\nbut you can tune them below if needed."))

    # Main frame
    subframeSbatch = customtkinter.CTkFrame(master=root)
    subframeSbatch.pack(side="top", fill="both", pady=6, padx=10)
    
    # Subframes
    time_limit(subframeSbatch, days, hours, minutes, sec)
    cpu_params(subframeSbatch, nb_cpu, mem_cpu)
    sbatch_fine_tuning(root)
    
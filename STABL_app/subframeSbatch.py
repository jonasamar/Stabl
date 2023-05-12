import customtkinter

from subwindows import show_message

from SubframeComponents.timeentry import time_entry
from SubframeComponents.cpuentry import cpu_entry
from SubframeComponents.sbatchfinetuning import sbatch_fine_tuning

def subframeSbatch_display(root, days, hours, minutes, sec, nb_cpu, mem_cpu):
    labelSbatch = customtkinter.CTkLabel(root, text="Sbatch file parameters *", font=("Roboto", 16))
    labelSbatch.pack(pady=6, padx=10)
    labelSbatch.bind("<Button-1>", lambda event : show_message("info", "In order to run your python script on Sherlock,\nyou need to create a.sbatch file.\nMost parameters can be left by default,\nbut you can tune them below if needed."))

    subframeSbatch = customtkinter.CTkFrame(master=root)
    subframeSbatch.pack(side="top", fill="both", pady=6, padx=10)
    
    time_entry(subframeSbatch, days, hours, minutes, sec)
    cpu_entry(subframeSbatch, nb_cpu, mem_cpu)
    sbatch_fine_tuning(root)
    
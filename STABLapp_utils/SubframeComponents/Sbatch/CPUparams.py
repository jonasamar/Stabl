#------------------------------------------------------------------------------------------------------------------------------
#
# Function : cpu_params
#
# Description :
#       - arguments : subframeSbatch, parameters linked to CPUs requirements for the job  
#       - effect : Display
#                   - a combobox to chose the number of CPUs required
#                   - a combobox to chose the memory per CPU required
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter

from STABLapp_utils.subwindows.MessageWindow import show_message

def cpu_params(subframeSbatch, nb_cpu, mem_cpu):    
    #nb_cpu
    subframeNcpu = customtkinter.CTkFrame(subframeSbatch, width=200, height=100)
    subframeNcpu.pack(side="left", fill="both", padx=(10,5), pady=5)
    
    labelpip = customtkinter.CTkLabel(subframeNcpu, text="Number of CPUs *")
    labelpip.pack(side="left", fill="both", padx=(10, 5))
    labelpip.bind("<Button-1>", lambda event : show_message("info","Number of CPUs Sherlock is going to mobilize for your job.\n\nFor those who don't know :\nA Central Processing Unit (CPU), or core, or CPU core, is the smallest\nunit in a microprocessor that can carry out computational tasks, that is,\nrun programs. Modern processors typically have multiple cores."))
                   
    comboboxpip = customtkinter.CTkComboBox(subframeNcpu, variable=nb_cpu, values=[str(i) for i in range(1, 11)], width=175, justify='center')
    comboboxpip.pack(side="left", fill="both", padx=10, pady=5)
    
    #mem_cpu
    subframeMemcpu = customtkinter.CTkFrame(subframeSbatch, width=200, height=100)
    subframeMemcpu.pack(side="left", fill="both", padx=(10,5), pady=5)
    
    labelpip = customtkinter.CTkLabel(subframeMemcpu, text="Memory per CPU *")
    labelpip.pack(side="left", fill="both", padx=(10, 5))
    labelpip.bind("<Button-1>", lambda event : show_message("info","Memory per CPU Sherlock is going to mobilize for your job.\n\nFor those who don't know :\nA Central Processing Unit (CPU), or core, or CPU core, is the smallest\nunit in a microprocessor that can carry out computational tasks, that is,\nrun programs. Modern processors typically have multiple cores."))
                   
    comboboxpip = customtkinter.CTkComboBox(subframeMemcpu, variable=mem_cpu, values=[str(2**i)+" GB" for i in range(7)], width=200, justify='center')
    comboboxpip.pack(side="left", fill="both", padx=10, pady=5)
    
    
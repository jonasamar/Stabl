#------------------------------------------------------------------------------------------------------------------------------
#
# Function : recap_sbatch_params
#
# Description :
#       - arguments : parameters linked to the sbatch file
#       - effect : Display the parameters of the sbatch file/ job selected by the user
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter

def recap_sbatch_params(root, days, hours, minutes, sec, nb_cpu, mem_cpu):
    
    labelSbatch = customtkinter.CTkLabel(root, justify='center', text='Sbatch file parameters', font=('Roboto', 14))
    labelSbatch.pack()  
    SubframeSbatch = customtkinter.CTkFrame(root)
    SubframeSbatch.pack(side='top', fill='both', padx=10, pady=6)
        
    labelTimeLimit = customtkinter.CTkLabel(SubframeSbatch, text=f'Time limit : {days.get()}-{hours.get()}:{minutes.get()}:{sec.get()}', justify='left')
    labelTimeLimit.pack(side='top', padx=10, pady=6, anchor="w")
    
    labelNbCPU = customtkinter.CTkLabel(SubframeSbatch, text='Number of CPUs : '+str(nb_cpu.get()), justify='left')
    labelNbCPU.pack(side='top', padx=10, pady=6, anchor="w")
    
    labelMemCPU = customtkinter.CTkLabel(SubframeSbatch, text='Memory per CPU type : '+str(mem_cpu.get()), justify='left')
    labelMemCPU.pack(side='top', padx=10, pady=6, anchor="w")
#------------------------------------------------------------------------------------------------------------------------------
#
# Function : time_limit
#
# Description :
#       - arguments : subframeSbatch, parameters linked to the time limit of the job  
#       - effect : Display
#                   - 4 textboxes to enter the time limit of the task (format : days-hours:minutes:sec)
#
#------------------------------------------------------------------------------------------------------------------------------

import customtkinter

from subwindows.MessageWindow import show_message

def time_limit(subframeSbatch, days, hours, minutes, sec):    
    subframeTime = customtkinter.CTkFrame(subframeSbatch, width=200, height=100)
    subframeTime.pack(side="top", fill="both", padx=10, pady=6)
    
    labelTime = customtkinter.CTkLabel(subframeTime, text="Time limit * [days - hours : min : sec]")
    labelTime.pack(side="left", fill="both", padx=10, pady=6)
    labelTime.bind("<Button-1>", lambda event : show_message("info","Sherlock will automatically stop running your script when the time limit is reached.\nMake sure it is big enough ! 2 days should be fine but you can\ntune this parameter if needed.\n\n Make sure minutes and seconds are written with two digits."))
                   
    daysentry = customtkinter.CTkEntry(subframeTime, textvariable=days, placeholder_text=days.get(), width=60, justify='center')
    daysentry.pack(side="left", fill="both", padx=5, pady=5)
    
    labeldayshours = customtkinter.CTkLabel(subframeTime, text=" - ")
    labeldayshours.pack(side="left", fill="both", padx=5, pady=5)
    
    hoursentry = customtkinter.CTkEntry(subframeTime, textvariable=hours, placeholder_text=hours.get(), width=60, justify='center')
    hoursentry.pack(side="left", fill="both", padx=5, pady=5)
    
    labelhoursmin = customtkinter.CTkLabel(subframeTime, text=" : ")
    labelhoursmin.pack(side="left", fill="both", padx=5, pady=5)
    
    minsentry = customtkinter.CTkEntry(subframeTime, textvariable=minutes, placeholder_text=minutes.get(), width=60, justify='center')
    minsentry.pack(side="left", fill="both", padx=5, pady=5)
    
    labelminsec = customtkinter.CTkLabel(subframeTime, text=" : ")
    labelminsec.pack(side="left", fill="both", padx=5, pady=5)
    
    secentry = customtkinter.CTkEntry(subframeTime, textvariable=sec, placeholder_text=sec.get(), width=60, justify='center')
    secentry.pack(side="left", fill="both", padx=5, pady=5)
    
    
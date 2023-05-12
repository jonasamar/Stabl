def write_sbatch(fsbatch, foldername, days, hours, minutes, sec):
    if days > 0:
        str_days = str(days) + '-'
    else:
        str_days = ""
    str_hours = str(hours)
    str_minutes = str(minutes)
    str_sec = str(sec)
    if len(str_minutes) == 1:
        str_minutes = "0"+str_minutes
    if len(str_sec) == 1:
        str_sec = "0"+str_sec
        
    fsbatch.write("#!/bin/bash\n")
    fsbatch.write(f"#SBATCH --job-name={foldername}\n")
    fsbatch.write("#SBATCH --time={str_days}{str_hours}:{str_minutes}:{str_sec}\n")
    fsbatch.write("#SBATCH --ntasks=1\n")
    fsbatch.write("#SBATCH --mem-per-cpu=2G\n")
    fsbatch.write(f"#SBATCH --output={foldername}.out\n")
    fsbatch.write(f"#SBATCH --error={foldername}.err\n")
    fsbatch.write("#SBATCH -p normal\n")
    fsbatch.write("#SBATCH -c 2\n")
    fsbatch.write("\n")
    fsbatch.write("module load python/3.9.0\n")
    fsbatch.write(f"python3 {foldername}.py\n")
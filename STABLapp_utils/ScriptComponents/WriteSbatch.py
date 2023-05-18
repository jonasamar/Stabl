#------------------------------------------------------------------------------------------------------------------------------
#
# Function : write_sbatch
#
# Description : fsbatch, foldername, days, hours, minutes, sec, nb_cpu, mem_cpu
#       - arguments : fsbatch (sbatch file) and sbatch file parameters
#       - effect : write in the sbatch file the code to run the python script with sherlock
#
#------------------------------------------------------------------------------------------------------------------------------

def write_sbatch(fsbatch, foldername, days, hours, minutes, sec, nb_cpu, mem_cpu):
    fsbatch.write("#!/bin/bash\n")
    fsbatch.write(f"#SBATCH --job-name={foldername}\n")
    fsbatch.write(f"#SBATCH --time={days}-{hours}:{minutes}:{sec}\n")
    fsbatch.write("#SBATCH --ntasks=1\n")
    fsbatch.write(f"#SBATCH --mem-per-cpu={str(mem_cpu).replace(' GB', '')}G\n")
    fsbatch.write(f"#SBATCH --output={foldername}.out\n")
    fsbatch.write(f"#SBATCH --error={foldername}.err\n")
    fsbatch.write("#SBATCH -p normal\n")
    fsbatch.write(f"#SBATCH -c {nb_cpu}\n")
    fsbatch.write("\n")
    fsbatch.write("module load python/3.9.0\n")
    fsbatch.write(f"python3 {foldername}.py\n")
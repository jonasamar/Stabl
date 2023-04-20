#!/bin/bash
#
#SBATCH --job-name=Tutorial_Notebook
#
#SBATCH --time=48:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=Tutorial_Notebook.out
#SBATCH --error=Tutorial_Notebook.err
#SBATCH -p normal
#SBATCH -c 1

module load python/3.6.1
module load py-numpy/1.19.2_py36
python3 Tutorial Notebook.ipynb



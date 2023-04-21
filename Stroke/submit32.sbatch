#!/bin/bash
#SBATCH --job-name=Pipeline_Bcells_PO_32cpus.py
#SBATCH --time=48:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=Pipeline_Bcells_PO_32cpus.out
#SBATCH --error=Pipeline_Bcells_PO_32cpus.err
#SBATCH -p normal
#SBATCH -c 32

module load python/3.9.0
python3 Pipeline_Bcells_PO.py



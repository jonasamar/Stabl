#!/bin/bash
#SBATCH --job-name=ProtCytofEgaTermData
#SBATCH --time=3-00:00:00
#SBATCH --qos=long
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=16G
#SBATCH --output=ProtCytofEgaTermData.out
#SBATCH --error=ProtCytofEgaTermData.err
#SBATCH -p normal
#SBATCH -c 2

module load python/3.9.0
python3 ProtCytofEgaTermData.py

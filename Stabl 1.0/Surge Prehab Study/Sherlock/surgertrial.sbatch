#!/bin/bash
#SBATCH --job-name=surgertrial
#SBATCH --time=2-00:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=16G
#SBATCH --output=surgertrial.out
#SBATCH --error=surgertrial.err
#SBATCH -p normal
#SBATCH -c 2

module load python/3.9.0
python3 surgertrial.py

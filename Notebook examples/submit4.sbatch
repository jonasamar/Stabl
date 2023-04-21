#!/bin/bash
#SBATCH --job-name=CFRNAUnivariate.py
#SBATCH --time=48:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=CFRNAUnivariate.out
#SBATCH --error=CFRNAUnivariate.err
#SBATCH -p normal
#SBATCH -c 2

module load python/3.9.0
python3 CFRNAUnivariate.py


#!/bin/bash
#SBATCH --job-name=COVD19test
#SBATCH --time=2-00:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=16G
#SBATCH --output=COVD19test.out
#SBATCH --error=COVD19test.err
#SBATCH -p normal
#SBATCH -c 2

module load python/3.9.0
python3 COVD19test.py

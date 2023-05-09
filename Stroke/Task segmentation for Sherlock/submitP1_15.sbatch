#!/bin/bash
#SBATCH --job-name=P1_15
#SBATCH --time=48:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=P1_15.out
#SBATCH --error=P1_15.err
#SBATCH -p normal
#SBATCH -c 2

module load python/3.9.0
python3 ExecutePipelineP1_15.py
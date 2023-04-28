#!/bin/bash
#SBATCH --job-name=Delta
#SBATCH --time=48:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=Delta.out
#SBATCH --error=Delta.err
#SBATCH -p normal
#SBATCH -c 2

module load python/3.9.0
python3 ExecutePipelineDelta.py
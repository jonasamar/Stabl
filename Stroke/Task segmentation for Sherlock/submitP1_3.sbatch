#!/bin/bash
#SBATCH --job-name=P1_3
#SBATCH --time=48:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=P1_3.out
#SBATCH --error=P1_3.err
#SBATCH -p normal
#SBATCH -c 2

module load python/3.9.0
python3 BenchmarksP1_3.py
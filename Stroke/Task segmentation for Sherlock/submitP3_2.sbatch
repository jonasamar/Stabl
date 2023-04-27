#!/bin/bash
#SBATCH --job-name=P3_2
#SBATCH --time=48:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=P3_2.out
#SBATCH --error=P3_2.err
#SBATCH -p normal
#SBATCH -c 2

module load python/3.9.0
python3 BenchmarksP3_2.py
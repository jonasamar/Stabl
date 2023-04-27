#!/bin/bash
#SBATCH --job-name=Delta_2
#SBATCH --time=48:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=Delta_2.out
#SBATCH --error=Delta_2.err
#SBATCH -p normal
#SBATCH -c 2

module load python/3.9.0
python3 BenchmarksDelta_2.py
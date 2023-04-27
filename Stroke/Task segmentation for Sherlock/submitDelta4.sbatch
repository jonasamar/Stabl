#!/bin/bash
#SBATCH --job-name=Delta_4
#SBATCH --time=48:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=Delta_4.out
#SBATCH --error=Delta_4.err
#SBATCH -p normal
#SBATCH -c 2

module load python/3.9.0
python3 BenchmarksDelta_4.py
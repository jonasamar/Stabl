#!/bin/bash
#SBATCH --job-name=SSIBenchmarks.py
#SBATCH --time=48:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=SSIBenchmark.out
#SBATCH --error=SSIBenchmarks.err
#SBATCH -p normal
#SBATCH -c 32

module load python/3.9.0
python3 SSIBenchmarks.py



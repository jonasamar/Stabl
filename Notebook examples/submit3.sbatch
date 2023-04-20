#!/bin/bash
#SBATCH --job-name=SyntheticBenchmarkRegression.py
#SBATCH --time=48:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=SyntheticBenchmarkRegression.out
#SBATCH --error=SyntheticBenchmarkRegression.err
#SBATCH -p normal
#SBATCH -c 32

python3 SyntheticBenchmarkRegression.py


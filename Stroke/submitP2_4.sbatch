#!/bin/bash
#SBATCH --job-name=P2_4
#SBATCH --time=48:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=P2_4.out
#SBATCH --error=P2_4.err
#SBATCH -p normal
#SBATCH -c 2

module load python/3.9.0
python3 BenchmarksP2_4.py
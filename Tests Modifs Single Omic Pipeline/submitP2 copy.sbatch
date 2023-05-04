#!/bin/bash
#SBATCH --job-name=NewSingleOmic
#SBATCH --time=48:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=NewSingleOmic.out
#SBATCH --error=NewSingleOmic.err
#SBATCH -p normal
#SBATCH -c 2

module load python/3.9.0
python3 NewSingle_omic.py
#!/bin/bash
#SBATCH --job-name=NewSingleOmic16G
#SBATCH --time=48:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=16G
#SBATCH --output=NewSingleOmic16G_oldv.out
#SBATCH --error=NewSingleOmic16G_oldv.err
#SBATCH -p normal
#SBATCH -c 4

module load python/3.9.0
python3 NewSingle_omic.py
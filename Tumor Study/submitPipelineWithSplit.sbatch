#!/bin/bash
#SBATCH --job-name=TumorPipelineWithSplit
#SBATCH --time=2-00:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=16G
#SBATCH --output=TumorPipelineWithSplit.out
#SBATCH --error=TumorPipelineWithSplit.err
#SBATCH -p normal
#SBATCH -c 4

module load python/3.9.0
python3 PipelineWithSplit.py
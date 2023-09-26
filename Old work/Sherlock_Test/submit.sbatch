#!/bin/bash
#SBATCH --job-name=Sherlock_Test
#SBATCH --time=00:01:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=2G
#SBATCH --output=Sherlock_Test.out
#SBATCH --error=Sherlock_Test.err
#SBATCH -p normal
#SBATCH -c 1

module load python/3.6.1
#pip3 install scikit-learn
#pip3 install pandas
#pip3 install numpy
#pip3 install joblib
#pip3 install tqdm
#pip3 install seaborn
#pip3 install matplotlib
#pip3 install knockpy

python3 Sherlock_Test.py



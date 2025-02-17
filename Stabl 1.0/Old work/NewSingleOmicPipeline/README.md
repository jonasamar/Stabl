# Folder Description

## Files

* submitNEWtest.sbatch :
Sbatch file required to execute NewSingle_Omic.py with Sherlock.

* NewSingleOmic16G_oldv.err :
Error file generated by Sherlock when executing the sbatch file.

* NewSingleOmic16G_oldv.out :
Output file generated by Sherlock when executing the sbatch file.

* NewSingle_Omic.py : 
File containing the single omic pipeline with cross validation modified to test multiple STABLs with different base_estimators at once.

## Result folders

* Results :
Folder containing the results of the new pipeline with L-RP (Lasso with Random Permutation) and L-KF (Lasso with Knock Off) on the COVID-19 dataset with only the 20 first samples.

* Results_all_data :
Folder containing the results of the new pipeline with L-RP (Lasso with Random Permutation) and L-KF (Lasso with Knock Off)on the whole COVID-19 dataset.

## Description of the changes and comments

* Changes from the original pipeline:
- single_omic_stabl_cv > new_single_omic_stabl_cv
- compute_score_table > new_compute_score_table
- cf lines of code with : # New pipeline

* Reported issues :
When I tried to run the same pipeline including the base_estimator EN05 (elastic net with l1_ratio=0.5), the pipeline took much longer (more than two days versus less than an hour with the two models indicated above). It might be because of the size of the dataset. I was also wondering if some part of the code could be parallelized ? (maybe it is already... but I am not very familiar with parallelization so I wanted to point it out).

* A work in progress :
The single omic pipeline has only been modified for binary tasks. Some more lines should be added to have the same Result folder for regression tasks. Then, we could try to apply the same modifications to the multi-omic pipeline.
Description of the STABLvsEN folder

Study:
We are looking for a small number of characteristics that most accurately predict whether a stroke patient is at risk for hemorrhage following a procedure to remove the clot that caused the stroke.
We have a cohort of 20 patients (10 hemorrhagic and 10 nonhemorrhagic) who all underwent the procedure. Three samples were taken from these patients: preoperatively, postoperatively, and 30 days postoperatively. 
The samples are all unstimulated and we have measurements of 12 reagents for 27 cell populations per sample.

Summary of data:
- 20 patients
- 3 time points
- 27 cell populations
- 12 reagent measurements

Method:
We ran the single_omic_stabl_cv pipeline with the following different parameters: 
Lasso Random Permutation
Lasso Knockoff
ElasticNet(alpha=0.5) Random permutation
ElasticNet(alpha=0.5) Knockoff

Result description:
1 - Lasso-based Stabl selected no features.
2 - The best AUC ROC obtained is for ElasticNet Knockoff: 0.76. But, in comparison, we noticed that ElasticNet ("normal") had an AUC ROC of 0.91, which is much higher...

Questions:
a - Are the signals found by STABL and ElasticNet similar? ie Are the features with the best selection frequencies the same?

Answer a: We notice that the selected features are the same. The difference is not explained by different feature choices between the two models (Feature comparison.png, Feature comparison.csv, Max STABLvsEN scores.csv)

b - ElasticNet naturally selects more features than STABL (Feature comparison.png, Feature comparison.csv, Max STABLvsEN scores.csv). Do the additional features that ElasticNet relies on seem as interesting as those common to STABL and ElasticNet?

Rep b: By a simple univariate boxplot analysis, it seems that the features selected by ElasticNet that are not taken into account by STABL allow significant differences in medians (STABL&EN features, STABL - EN features, EN - STABL features).

Open question: Wouldn't the results obtained lead us to consider a less sparse model? Are there any parameters we could play with to make Stabl approach the performance of ElasticNet while remaining sparse?

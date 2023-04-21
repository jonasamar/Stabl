from stabl.preprocessing import remove_low_info_samples
import pandas as pd
from scipy.stats import spearmanr
import numpy as np
import csv

# Importing the input dataframe
X = pd.read_csv("../Sample Data/CFRNA/cfrna_dataFINAL.csv", index_col=0)

# Importing patients' ID
IDs = pd.read_csv("../Sample Data/CFRNA/ID.csv", index_col=0)

# Importing the Preeclampsia outcome
y = pd.read_csv("../Sample Data/CFRNA/all_outcomes.csv", index_col=0)
X = remove_low_info_samples(X)  # Removing samples without any information
X = X.apply(lambda x: np.log2(x+1))  # Applying the log2(x+1) transformation

IDs = IDs.loc[X.index]
y = y.loc[X.index].Preeclampsia

Spearmancorr = {}

features = X.columns

for feature in features:
    
    corr, pval = spearmanr(X[feature], y)
    Spearmancorr[feature] = [corr, pval]

SpearmanPvalue = pd.DataFrame(Spearmancorr).T
SpearmanPvalue.columns = ['Spearman corr', 'pvalue']
SpearmanPvalue.sort_values('pvalue', inplace=True)
SpearmanPvalue.to_csv('../Results Biobank SSI/Summary/SpearmanCorrelationsPval.csv', index=True)

from stabl.visualization import scatterplot_features

scatterplot_features(
        SpearmanPvalue[:10].index,
        X,
        y,
        show_fig=False,
        export_file=True,
        path='../Results Biobank SSI/Univariate')
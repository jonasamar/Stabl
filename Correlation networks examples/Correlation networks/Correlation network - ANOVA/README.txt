- FOLDER "Test figures": Contains two test figures one using original trajectories, the other one has smoothed trajectories (Smoothed with a spline). The description of the figure is in the folder.

- FOLDER "Clusters Trajectories": Contains the trajectories of each cluster. In the FOLDER "medians only": for each cluster we have the original trajectories and the smoothed one. In each figure, the solid line is the median of NO POCD patients and the doted one is the median of POCD patients. The filled area is the interquartile range for each group. In the FOLDER "Medians & all features" we added the individual trajectory of each feature in light gray (dotted line for POCD, solid line for NO POCD). As before we can find the original curves and the smoothed version.

- FOLDER "Top features Trajectories": contains the trajectories of the top feature in terms of ANOVA p-value of each cluster. Same as before we represent the median and the interquartile range for each group (POCD and NO POCD), and we have a smoothed version.

- FILE "correlation networks.pdf": Representation of the trajectories from the correlation network of the baseline CyTOF features for all timepoints on a t-SNE layout. Each node represents an immune feature of the CyTOF dataset, with both intracellular markers and frequencies of each cell type. The size of each node varies according to the p-value of the main effect of POCD calculated from an ANOVA. Edges represent a correlation coefficient R>0.7 between two features. Names of features which ANOVA p-value ≤ 0.01 are displayed in the correlation networks. Features are further clustered using k-means and the number of clusters is optimized using the silhouette score.

- FILE "correlation networks no annot.pdf": Same as before but without any feature name displayed!

- FILE "annotations.pdf": The annotations figure with all the names of the features and cluster numbers.

- FILE "df_tsne.csv": csv file containing the coordinates of the t-SNE layout, the cluster and the ANOVA p-value for each feature.


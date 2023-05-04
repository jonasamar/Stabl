In "with_pure_data", the pipeline is run only on the data indicated after "pure" in the name of each file (for example "Correlation Network pure P1" is run only on the data corresponding to time='P1', even the clustering part of the pipeline).

In "with_same_clusters" the pipeline is run with the clustering always based on the whole data (Delta + P1 + P2 + P3). That is why we can always see the same clusters in each file which makes it easier to compare with the others.

In "new_CN", we apply the same pipeline but we concatenate the different datasets (Delta, P1, P2, P3) on columns so that the features that are considered are : cellpopulation_time_reagent.

"Correlatiion Network all data" is the result of the pipeline run on all the data (Delta + P1 + P2 + P3).

In "Umap", the projection of data on a two-dimensional space is done with Umap instead of TSNE.

Any questions:
* send message : +33 6 52 32 26 44
* send email : jonas.ns.amar@gmail.com
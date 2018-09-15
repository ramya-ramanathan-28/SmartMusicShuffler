import pandas as pd
df= pd.read_csv("features.csv", sep='\t', encoding='utf-8')

#Affinity Propogation- method of clustering 2

from sklearn.cluster import AffinityPropagation
af = AffinityPropagation(preference=-50).fit(df)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_
print(labels)
no_clusters = len(cluster_centers_indices)

print('Estimated number of clusters: %d' % no_clusters)

from sklearn import cluster
#Agglomerative clustering - method of clustering 3
ward = cluster.AgglomerativeClustering(
        n_clusters=8, linkage='ward',
        connectivity=connectivity)
ward.fit(X)

print(ward.labels_)

#spectral clustering 
spectral = cluster.SpectralClustering(
        n_clusters=8, eigen_solver='arpack',
        affinity="nearest_neighbors")
spectral.fit(X)

print(spectral.labels_)

#Minibatch k-means clustering 
from sklearn.cluster import MiniBatchKMeans
mbk = MiniBatchKMeans(init='k-means++', n_clusters=8, batch_size=100,
                      n_init=10, max_no_improvement=10, verbose=0,
                      random_state=0)
mbk.fit(X)

print(mbk.labels_)



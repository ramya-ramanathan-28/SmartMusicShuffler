import pickle
import pandas as pd



def cluster():
        #df = extract_classify()
        df = pd.read_csv("data/features.csv")
        #Clustering using HDBSCAN
        #import hdbscan
        global new_df
        new_df = df[df.columns[2:]]
        '''
        clusterer = hdbscan.HDBSCAN(algorithm='best', alpha=1.0, approx_min_span_tree=True,gen_min_span_tree=False, leaf_size=40, metric='euclidean', min_cluster_size=5, min_samples=None, p=None)
        
        clusterer.fit(new_df)
        print(clusterer.labels_)
        df['cluster_labels'] = clusterer.labels_
        '''
        from sklearn.cluster import AffinityPropagation
        af = AffinityPropagation(preference=-50).fit(new_df)
        cluster_centers_indices = af.cluster_centers_indices_
        labels = af.labels_
        print(labels)
        df['cluster_labels'] = labels
        no_clusters = len(cluster_centers_indices)

        centers = "clustering.data"
        fw = open(centers, "wb")
        pickle.dump(cluster_centers_indices, fw)
        fw.close()
        
        df.to_csv("data/features.csv", index = False)
        
cluster()

#MUSIC FEATURE EXTRACTION USING LIBROSA LIBRARY
import librosa
import librosa.display
import numpy as np
import os
import os.path
import pandas as pd

#df = pd.DataFrame(columns=['Name','Beat','RMSE','MFCC', 'Tonality'])
list_df=[]
for dirpath, dirnames, filenames in os.walk("."):
    for filename in [f for f in filenames if f.endswith(".mp3")]:
        
        i= os.path.join(dirpath, filename)
        #Loading music file
        #y = audio time series, sr = sampling rate of y
        print(i)
        y, sr = librosa.load(i)


        #Extracting Tempo
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

        #Calculation of average rmse 
        rmses=librosa.feature.rmse(y=y)
        #print(rmse)
        rmse=0
        n=0
        for item in rmses:
            for x in item:
                rmse+=x
                n=n+1
        rmse=rmse/n
        print('Estimated rmse: {:.2f} '.format(rmse))

        #Calculating average mfcc
        librosa.feature.mfcc(y=y, sr=sr)
        mfccs = librosa.feature.mfcc(y=y, sr=sr)
        mfcc=0
        n=0
        for item in mfccs:
            for x in item:
                mfcc+=x
                n=n+1
        mfcc=mfcc/n
        print('Estimated mfcc: {:.2f} '.format(mfcc))

        #computing tonal centroid features
        y = librosa.effects.harmonic(y)
        tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
        tonal=0
        n=0
        for item in tonnetz:
            for x in item:
                tonal+=x
                n=n+1
        tonal=tonal/n
        print('Estimated tonality: {:.2f} '.format(tonal))
        list_df.append([i, tempo, rmse, mfcc, tonal])

df = pd.DataFrame(list_df,columns=['Name','Beat','RMSE','MFCC', 'Tonality'])
print(df)
df.to_csv("features.csv", sep='\t', encoding='utf-8')

#Clustering using HDBSCAN
import hdbscan
clusterer = hdbscan.HDBSCAN(algorithm='best', alpha=1.0, approx_min_span_tree=True,gen_min_span_tree=False, leaf_size=40, metric='euclidean', min_cluster_size=5, min_samples=None, p=None)
clusterer.fit(df)
print(clusterer.labels_)

#MUSIC FEATURE EXTRACTION USING LIBROSA LIBRARY
import librosa
import librosa.display
import numpy as np
import os
import pickle
import os.path
import pandas as pd
from scipy.io.wavfile import read
from scipy.io.wavfile import write
from scipy import signal

new_df = []
list_df=[]
'''
for dirpath, dirnames, filenames in os.walk("./songs"):
    for filename in [f for f in filenames if f.endswith(".mp3")]:
'''

def extract_classify():
    print ('Reading data...')
    temp_df = pd.read_csv('data/song_data.csv')
    IDs = temp_df['ID'].tolist()
    paths = temp_df['Path'].tolist()
    for i, j in zip(paths, IDs):
        print ()
        #i= os.path.join(dirpath, filename)
        print(i)
        
        '''
        #noise removal-high pass, low pass, both or none?
        from pydub import AudioSegment
        sound = AudioSegment.from_mp3(i)
        sound.export("data/file.wav", format="wav")
        (Frequency, array) = read('data/file.wav')
        b,a = signal.butter(5, 1000/(Frequency/2), btype='highpass')
        filteredSignal = signal.lfilter(b,a,array)
        c,d = signal.butter(5, 380/(Frequency/2), btype='lowpass') 
        newFilteredSignal = signal.lfilter(c,d,filteredSignal)
        write("data/file2.wav", Frequency, newFilteredSignal)
        import subprocess
        subprocess.call(['ffmpeg','-y', '-i', 'file2.wav','FilteredMusicfile.mp3'])
        sound = AudioSegment.from_wav("data/file2.wav")
        sound.export("data/FilteredMusicfile.mp3", format="mp3")
        y, sr = librosa.load("data/FilteredMusicfile.mp3")
        '''
        
        #Loading music file
        #y = audio time series, sr = sampling rate of y
       
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
        list_df.append([j, i, tempo, rmse, mfcc, tonal])


    #Making dataset by using pandas
    df = pd.DataFrame(list_df,columns=['ID', 'Name','Beat','RMSE','MFCC', 'Tonality'])
    global new_df
    new_df = df[df.columns[2:]]
    print(df)
    df.to_csv("data/features.csv", index = False)
    return df
    #df.to_csv("features.csv", sep='\t', encoding='utf-8')


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
        



#MUSIC FEATURE EXTRACTION USING LIBROSA LIBRARY
import librosa
import librosa.display
import numpy as np
import os
import os.path
import pandas as pd
from scipy.io.wavfile import read
from scipy.io.wavfile import write
from scipy import signal

list_df=[]
for dirpath, dirnames, filenames in os.walk("./songs"):
    for filename in [f for f in filenames if f.endswith(".mp3")]:
        
        i= os.path.join(dirpath, filename)
        print(i)
        
        #noise removal-high pass, low pass, both or none?
        from pydub import AudioSegment
        sound = AudioSegment.from_mp3(i)
        sound.export("file.wav", format="wav")
        (Frequency, array) = read('file.wav')
        b,a = signal.butter(5, 1000/(Frequency/2), btype='highpass')
        filteredSignal = signal.lfilter(b,a,array)
        c,d = signal.butter(5, 380/(Frequency/2), btype='lowpass') 
        newFilteredSignal = signal.lfilter(c,d,filteredSignal)
        write("file2.wav", Frequency, newFilteredSignal)
        import subprocess
        subprocess.call(['ffmpeg','-y', '-i', 'file2.wav','FilteredMusicfile.mp3'])
        sound = AudioSegment.from_wav("file2.wav")
        sound.export("FilteredMusicfile.mp3", format="mp3")
        y, sr = librosa.load("FilteredMusicfile.mp3")
        
        
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
        list_df.append([i, tempo, rmse, mfcc, tonal])


#Making dataset by using pandas
df = pd.DataFrame(list_df,columns=['Name','Beat','RMSE','MFCC', 'Tonality'])
new_df = df[df.columns[1:]]
print(df)
df.to_csv("features.csv", sep='\t', encoding='utf-8')

#Clustering using HDBSCAN
import hdbscan
clusterer = hdbscan.HDBSCAN(algorithm='best', alpha=1.0, approx_min_span_tree=True,gen_min_span_tree=False, leaf_size=40, metric='euclidean', min_cluster_size=5, min_samples=None, p=None)
clusterer.fit(new_df)
print(clusterer.labels_)

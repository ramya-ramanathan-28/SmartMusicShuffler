import pickle
import random
import math
import pandas as pd
from predictor import get_next_number
#from constants import Constants

#const = Constants()


queue_feature_mapping = {}

cur_feature_seq = ''

def calculateDistance(x1,x2, x3, x4, y1, y2, y3, y4):  
     dist = math.sqrt((y1 - x1)**2 + (y2 - x2)**2 + (y3 - x3)**2 + (y4 - x4)**2 )  
     return dist

def return_distance(features):
        fd = open("clustering.data", 'rb')
        centers= pickle.load(fd)
        df = pd.read_csv('data/features.csv')
        min_dist = 999
        min_center = 0
        for c in centers :
                item = df.loc[df['ID'] == c].values
                #print (item[0])
                dist = calculateDistance(item[0][2], item[0][3], item[0][4], item[0][5], features[0], features[1], features[2], features[3])
                if  dist < min_dist:
                        min_dist = dist
                        min_center = c

        return df.loc[df['ID']== min_center]['cluster_labels'].values[0]
        

def return_song(cluster_number):
        df = pd.read_csv('data/features.csv')
        df = df.loc[df['cluster_labels'] == cluster_number]
        dfList = df['ID'].tolist()
        return random.choice(dfList)


def returnCluster(songID):
        df = pd.read_csv('data/features.csv')
        cluster = df.loc[df['ID'] == int(songID)]
        cluster = cluster['cluster_labels'].tolist()[0]
        return cluster

def returnFeatures(cluster_number):
        df = pd.read_csv('data/features.csv')
        df = df.loc[df['cluster_labels'] == cluster_number]
        df_new = df[['Beat', 'MFCC', 'RMSE', 'Tonality']].copy()
        return df_new.values.tolist()

def get_feature_values_hit(features_dropped):
        best_values = [0 for x in range(4)]
        global cur_feature_seq
        if (len(cur_feature_seq)>100):
                cur_feature_seq.pop(0)

        for i in range (0,4):
                if i not in features_dropped:
                        best_values[i] = get_next_number(cur_feature_seq[i], cur_feature_seq[i][:3],0)
                        #second_best_values[i] = get_second(cur_seq[:4])
                else:
                        best_values[i]= random.randint(1,5)
                        #second_best_values[i]=random()%4

        return best_values

def get_36_feature_numbers_miss(best_values, second_best_values, features_dropped):
     
        global cur_feature_seq
        global queue_feature_mapping
        song_queue =[]
        print ()
        print ("BEST VALUES")
        print (best_values)
        print ()
        #best_values = best_values[0]
        k=0
        for i in range(0,4):
                temp= best_values[i]
                best_values[i] = second_best_values[i]
                song_queue.append(best_values)
                best_values[i] = temp
                queue_feature_mapping[k]= [i]
                k=k+1
  
        for i in range(0,4):
                temp1 = best_values[i]
                best_values[i] = second_best_values[i]
                for j in range(i+1,4):
                        temp2 = best_values[j]
                        best_values[j] = second_best_values[j]
                        song_queue.append(best_values)
                        best_values[j] = temp2
                best_values[i] = temp1
                queue_feature_mapping[k]= [i,j]
        return song_queue


def predict(song_id, song_listened, i, CHOSEN):
        cluster_number = returnCluster(song_id)
        feature_values = returnFeatures(cluster_number)

        inputFile = 'start.data'
        fd = open(inputFile, 'rb')
        features_dropped = pickle.load(fd)
        global cur_feature_seq
        cur_feature_seq = pickle.load(fd)
        feature_weight =pickle.load(fd)
        #pickle.load(global cur_seq, fd)
        #pickle.load(global seq_count, fd)
        song_queue = pickle.load(fd)
        #pickle.load(current_song_cluster_number, fd)
        second_best_values = [0 for x in range(4)]
        next_song_feature_values = get_feature_values_hit(features_dropped)
        print (next_song_feature_values)
        print ()
        print ("SONG QUEUE")
        print (song_queue)
        print ()

        if i==-1:

                if (CHOSEN):
                        cur_feature_seq[i] = cur_feature_seq[i] + '{}'.format(feature_values[i])

                if (song_listened and not CHOSEN):
                        for i in range(0, 4):
                            cur_feature_seq[i] = cur_feature_seq[i] + '{}'.format(next_song_feature_values[i])

                elif (not song_listened and not CHOSEN):
                        for i in range (0,4):
                            if i not in features_dropped:
                                second_best_values[i] = get_next_number(cur_feature_seq[i], cur_feature_seq[i][:3],1)
                            else:
                                second_best_values[i]=random.randint(1,5)
                        song_queue = get_36_feature_numbers_miss (next_song_feature_values, second_best_values, features_dropped)
                        i= i + 1
                        #next_song_feature_values = get_feature_values_hit(features_dropped)
                        #cluster_num = features_to_cluster(next_song_feature_values)

        else:
                if(CHOSEN):
                        cur_feature_seq[i] = cur_feature_seq[i] + '{}'.format(feature_valules[i])
                        i=-1
                        song_queue = []
                if (not song_listened and not CHOSEN):
                        i = i + 1
                        if i>16:
                                i=0
          
                if (song_listened and not CHOSEN):
                        for j in range(0,4):
                                cur_feature_seq[j] = cur_feature_seq[j] + '{}'.format(song_queue[i][j])
                        if len(queue_feature_mapping[i])==1:
                                feature_weight[i] = feature_weight[i] + 1
                                if feature_weight[i]>50:
                                        features_dropped.append(i)
                        else:
                                k=28
                                t=1
                                s=6
                                l=35
                                for j in range(0,4):
                                         if (i>=l):
                                                  feature_weight[s] = feature_weight[s] + 1
                                                  if feature_weight[s]>thresh:
                                                           features_dropped.append(s)
                                                  feature_weight[i-k] = feature_weight[i-k] + 1
                                                  if feature_weight[i-k]>thresh:
                                                           features_dropped.append(i-k)
                                                           break
                                                  k=k-t
                                                  t=t+1
                                                  s=s-1
                                                  l=l-t
                        i=-1
        next_song_feature_values = get_feature_values_hit(features_dropped)
        cluster_num = return_distance(next_song_feature_values)

        outputFile = 'start.data'
        fw = open(outputFile, 'wb')
        pickle.dump(features_dropped, fw)
        pickle.dump(cur_feature_seq, fw)
        pickle.dump(feature_weight, fw)
        #pickle.dump(cur_seq, fw)
        #pickle.dump(seq_count, fw)
        pickle.dump(song_queue, fw)
        #pickle.dump(current_song_cluster_number, fw)
        fw.close()
                
        return return_song(cluster_num), i

predict(10, 0, -1, True)

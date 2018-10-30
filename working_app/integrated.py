from predictor import get_next_number, plot_curve


def get_feature_values_hit(features_dropped):
    if (len(cur_feature_seq)>100):
        cur_feature_seq.pop(0)

    for i in range (0,8):
        if i not in features_dropped:
            best_values[i] = get_next_number(cur_feature_seq[i], cur_feature_seq[i][:3],0)
            #second_best_values[i] = get_second(cur_seq[:4])
        else:
            best_values[i]= random()%4
            #second_best_values[i]=random()%4

    return best_values

def get_36_feature_numbers_miss(best_values, second_best_values, features_dropped):
    song_queue=[]
    for i in range(0,8):
        temp= best_values[i]
        best_values[i] = second_best_values[i]
        song_queue.append(best_values)
        best_values[i] = temp

    for i in range(0,8):
        temp1 = best_values[i]
        best_values[i] = second_best_values[i]
        for j in range(1,8):
            temp2 = best_values[j]
            best_values[j] = second_best_values[j]
            song_queue.append(best_values)
            best_values[j] = temp2
        best_values[i] = temp1
    return song_queue


def get_next_song(song_id):

    inputFile = 'data/start.data'
    fd = open(inputFile, 'rb')
    pickle.load(features_dropped, fd)
    global cur_feature_seq
    pickle.load(cur_feature_seq, fd)
    pickle.load(feature_weight, fd)
    #pickle.load(global cur_seq, fd)
    #pickle.load(global seq_count, fd)
    #pickle.load(song_queue, fd)
    #pickle.load(current_song_cluster_number, fd)

    next_song_feature_values = get_feature_values_hit(features_dropped)
    #song_listened = play(next_song_feature_values)
    ID = get_song_ID(next_song_feature_values)
    return ID


def song_listened()
    if (song_listened):
        #features_of_song = get_features_from_clusters (next_song_cluster_number)
        for i in range(0, 8):
            cur_feature_seq[i].append(next_song_feature_values[i])

    else:
        for i in range (0,8):
            if i not in features_dropped:
                best_values[i] = get_next_number(cur_feature_seq[i], cur_feature_seq[i][:3],0)
                second_best_values[i] = get_next_number(cur_feature_seq[i], cur_feature_seq[i][:3],1)
        else:
            best_values[i]= random()%4
            second_best_values[i]=random()%4
        song_queue = get_36_feature_numbers_miss (best_values, second_best_values, features_dropped)
        for i in range(0, 36):
            song_listened = play(song_queue[i])
            if (not song_listened):
                continue
            else:
                #features_of_song = get_features_from_clusters (next_song_cluster_number)
                for j in range(0,8):
                    cur_feature_seq[j].append(song_queue[i][j])
                if i<=7:
                    feature_weight[i]+=1
                    if feature_weight[i]>thresh:
                        features_dropped.append(i)
                else:
                    k=28
                    t=1
                    s=6
                    l=35
                    for j in range(0,7):
                        if (i>=l):
                           feature_weight[s]+=1
                           if feature_weight[s]>thresh:
                              features_dropped.append(s)
                           feature_weight[i-k]+=1
                           if feature_weight[i-k]>thresh:
                              features_dropped.append(i-k)
                           break
                        k=k-t
                        t+=1
                        s-=1
                        l=l-t
                break

    outputFile = 'data/start.data'
    fw = open(outputFile, 'wb')
    pickle.dump(features_dropped, fw)
    pickle.dump(cur_feature_seq, fw)
    pickle.dump(feature_weight, fw)
    #pickle.dump(cur_seq, fw)
    #pickle.dump(seq_count, fw)
    #pickle.dump(song_queue, fw)
    #pickle.dump(current_song_cluster_number, fw)
    fw.close()

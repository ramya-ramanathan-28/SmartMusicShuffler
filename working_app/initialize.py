import pickle

features_dropped = []
cur_feature_seq= ['111', '111', '111', '111', '111', '111']
#cur_seq = []
song_queue = []
feature_weight = [0, 0, 0, 0, 0, 0]
#current_song_cluster_number = 0

outputFile = 'start.data'
fw = open(outputFile, 'wb')
pickle.dump(features_dropped, fw)
pickle.dump(cur_feature_seq, fw)
pickle.dump(feature_weight, fw)
#pickle.dump(cur_seq, fw)
#pickle.dump(seq_count, fw)
pickle.dump(song_queue, fw)
fw.close()

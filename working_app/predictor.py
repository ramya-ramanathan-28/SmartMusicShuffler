#This is the code for the prediction sub module, which predicts the number that follows a sequence of given numbers using a
#recursive PPM (Prediction by Partial Matching) approach.

import re
import matplotlib.pyplot as plt
import pickle

def find_probability(subseq, escape_prob):
    """
    This function calculates the probability of each of the numbers following the given subsequence and calls itself recursively
    with a smaller subsequence if there is a probability for an escape character to follow

    Args:

    subseq: a string for which the probabilities of each character to be its following character is to be found 
    escape_prob: the probablity of an escape character folllowing the higher order subsequence which is to be distributed among
	         all characters w.r.t. probabilities of characters folllowing the current subsequence 
    
    """
    inputFile = 'probdata.data'
    fd = open(inputFile, 'rb')
    sequence = pickle.load(fd)
    prob_1 = pickle.load(fd)
    prob_2 = pickle.load(fd)
    prob_3 = pickle.load(fd)
    prob_4 = pickle.load(fd)
    list_of_initial_escapes = pickle.load(fd)
    last3 = pickle.load(fd)

    #sequence, prob_1, prob_2, prob_3, prob_4, list_of_initial_escapes
    no_of_1s, no_of_2s, no_of_3s, no_of_4s, no_of_escapes = (0,0,0,0,0)
    indices=[m.start() for m in re.finditer('(?={})'.format(subseq), '{}'.format(sequence))]
    #list=[]
    for index in indices:
        follows= sequence[index + len(subseq)]
        if (follows == '1'):
            no_of_1s= no_of_1s + 1
        if (follows == '2'):
            no_of_2s= no_of_2s + 1
        if (follows == '3'):
            no_of_3s= no_of_3s + 1
        if (follows == '4'):
            no_of_4s= no_of_4s + 1
        if (follows == 'P') and ((index + len(subseq)) not in list_of_initial_escapes):
            list_of_initial_escapes.append(index + len(subseq))
            no_of_escapes= no_of_escapes + 1
    total_occurances = no_of_1s + no_of_2s + no_of_3s + no_of_4s + no_of_escapes	
    prob_1= prob_1 + (escape_prob * (no_of_1s/total_occurances))
    prob_2= prob_2 + (escape_prob * (no_of_2s/total_occurances))
    prob_3= prob_3 + (escape_prob * (no_of_3s/total_occurances))
    prob_4= prob_4 + (escape_prob * (no_of_4s/total_occurances))
    if no_of_escapes>0:
        if len(subseq)>1:
            outputFile = 'probdata.data'
            fw = open(outputFile, 'wb')
            pickle.dump(sequence, fw)
            pickle.dump(prob_1, fw)
            pickle.dump(prob_2, fw)
            pickle.dump(prob_3, fw)
            pickle.dump(prob_4, fw)
            pickle.dump(list_of_initial_escapes, fw)
            pickle.dump(last3, fw)            
            fw.close()
            find_probability(last3[4-len(subseq):3], (no_of_escapes/total_occurances) * escape_prob)
        else:
            prob_1 = prob_1 + ((no_of_escapes/total_occurances) * escape_prob)/4 
            prob_2 = prob_2 + ((no_of_escapes/total_occurances) * escape_prob)/4 
            prob_3 = prob_3 + ((no_of_escapes/total_occurances) * escape_prob)/4 
            prob_4 = prob_4 + ((no_of_escapes/total_occurances) * escape_prob)/4 
            outputFile = 'probdata.data'            
            fw = open(outputFile, 'wb')
            pickle.dump(sequence, fw)
            pickle.dump(prob_1, fw)
            pickle.dump(prob_2, fw)
            pickle.dump(prob_3, fw)
            pickle.dump(prob_4, fw)
            pickle.dump(list_of_initial_escapes, fw)
            pickle.dump(last3, fw)            
            fw.close()


def get_next_number(sequence, last3, first_or_second):
    sequence="2P23323323332P1131432P3234322432P"
    last3= "432"
    list_of_initial_escapes=[]
    prob_1, prob_2, prob_3, prob_4 = (0.0, 0.0, 0.0, 0.0)
    outputFile = 'probdata.data'
    fw = open(outputFile, 'wb')
    pickle.dump(sequence, fw)
    pickle.dump(prob_1, fw)
    pickle.dump(prob_2, fw)
    pickle.dump(prob_3, fw)
    pickle.dump(prob_4, fw)
    pickle.dump(list_of_initial_escapes, fw)
    pickle.dump(last3, fw)
    fw.close()
    find_probability(last3, 1) 
    inputFile = 'probdata.data'
    fd = open(inputFile, 'rb')
    sequence = pickle.load(fd)
    prob_1 = pickle.load(fd)
    prob_2 = pickle.load(fd)
    prob_3 = pickle.load(fd)
    prob_4 = pickle.load(fd)
    list_of_initial_escapes = pickle.load(fd)
    last3 = pickle.load(fd)
  
    print ("The probabilities are: {}  {}  {}  {}".format(prob_1, prob_2, prob_3, prob_4))
      
    list_of_probs= [prob_1, prob_2, prob_3, prob_4]
    list_of_regions=[1,2,3,4]
    for i in range(0, 4):
        for j in range(0, 4-i-1):
            if list_of_probs[j] > list_of_probs[j+1] :
                list_of_probs[j], list_of_probs[j+1] = list_of_probs[j+1], list_of_probs[j]
                list_of_regions[j], list_of_regions[j+1] = list_of_regions[j+1], list_of_regions[j]
    if first_or_second==0:
        return list_of_regions[3]         
    else:
        return list_of_regions[2]

#get_next_number("456666","444",0)
#print ("The probabilities are: {}  {}  {}  {}".format(prob_1, prob_2, prob_3, prob_4))

"""
#plotting the graph showing how the curve could vary and what are the probabilities accosiated 
numbers=[]
numbers2=[]
numbers3=[]
numbers4=[]
pauses=[]
i=0
for number in sequence:
    if not number == "P":
        numbers.append(int(number))
        numbers2.append(int(number))
        numbers3.append(int(number))
        numbers4.append(int(number))
    else:
        i=i-1
        pauses.append(i)
    i=i+1
numbers.append(1)
numbers2.append(2)
numbers3.append(3)
numbers4.append(4)
plt.title('Pattern of feature regions for songs played by user and prediction of next value')
plt.ylabel('region number for a selected feature')
plt.xlabel('song number')
plt.grid(True)
Y=[0,4.5]
has_label=True
for value in range(len(pauses)-1):
    X=[pauses[value] + 0.5, pauses[value] + 0.5]
    if has_label:
        plt.plot(X,Y,color="brown",label="Breaks",linestyle="--")
        has_label=False
    else:
        plt.plot(X,Y,color="brown",linestyle="--")

plt.plot(numbers,color="red",label="P={}".format(prob_1),marker="*")
plt.plot(numbers2,color="blue",label="P={}".format(prob_2),marker="o")
plt.plot(numbers3,color="green",label="P={}".format(prob_3),marker="X")
plt.plot(numbers4,color="yellow",label="P={}".format(prob_4),marker="P")

plt.legend()
plt.show()
"""

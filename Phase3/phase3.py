# %%
from collections import defaultdict
from collections import Counter
from multiprocessing.sharedctypes import Value
from optparse import Values
import os
import math
import time
import sys
input_path='files'
global_map = defaultdict(list)

def word_search(search_word):
    res = []
    tobe_sorted = []
    if(len(global_map[search_word])<=10):
        for key , value in global_map[search_word]:
            res.append((key,value))
        return res
    else:
        for item in global_map[search_word]:
            for key, value in item.items():
     
               tobe_sorted.append((key, value))
    tobe_sorted = sorted(tobe_sorted, key = lambda x : x[1])
    for i in reversed(range(len(tobe_sorted)-10, len(tobe_sorted))):
        res.append((tobe_sorted[i][0],tobe_sorted[i][1]))
    return res


# %%
#Function to write posting file
def generate_output_file(filename,output_dir_path,global_map):
    filepath = os.path.join(output_dir_path, filename)
    with open(filepath, "w") as file:
        for key, value in global_map.items():
            for i in range(len(value)):
                for doc_num,tfidf in value[i].items():
                    file.write("{} {}\n".format(doc_num,tfidf))
        file.close()

# %%
#to write the dictionary file
def generate_output_file_2(filename,output_dir_path,global_map):
    filepath = os.path.join(output_dir_path, filename)
    i=1
    with open(filepath, "w") as file:
        for key, value in global_map.items():
            file.write("{} \n{} \n{}\n".format(key,len(value),i))
            i+=len(value)        
        file.close()

# %%
#storing each word from stopwords list to a dictionary to compare 
test_file = open('stopwords.txt','r',encoding='unicode_escape') 
stopwords_string = test_file.read()
stopwards = dict(Counter(stopwords_string.split()))
#preparing a dictionary for entire corpus
global_test_file = open('out-gloabal_op_1.txt','r',encoding='unicode_escape') 
global_string = global_test_file.read()
corpus = dict(Counter(global_string.split()))

# %%
def preprocessing(time_intervals,final_time):
    dfhm={}
    i=0
    input_path = 'files'
    curr_time=0.0 #to hold the time
    for file_n in os.listdir(input_path):
        filepath = os.path.join(input_path, file_n)
        start_time = time.time() #recording the time
        myfile = open(filepath, 'r') 
        for line in myfile:
            k, v = line.strip().split(' ')
            item_k = k.strip()
            item_v = int(v.strip())
            dfhm[item_k] = 1+ dfhm.get(item_k,0) #taking global count for a particular key
    j=0
    for j, filename in enumerate (os.listdir(input_path)): #fetching each file
        filepath = os.path.join(input_path, filename)
        myfile = open(filepath, 'r')
        curr_dict = {}
        for line in myfile: #fetching key value from each file
            k, v = line.strip().split(' ')
            item_k = k.strip()
            item_v = int(v.strip())
            if item_k not in stopwards or len(item_k)>1: #checking conditions from preprocessing
                curr_dict[item_k] = 1+ curr_dict.get(item_v,0)
        myfile.close()
        for key, val in curr_dict.items():
            tf= val/len(curr_dict) #calculating term frequency
            df=dfhm[key] #document frequency
            idf=math.log(503/df) #inverse document frequncy
            tfidf=tf*idf
            global_map[key].append({j+1 : tfidf})
        stop_time = time.time() - start_time #stopped recording time
        curr_time += stop_time
        if time_intervals and i+1 == time_intervals[0]:
            final_time += curr_time
            curr_time=0
            time_intervals.pop(0)
        i+=1

# %%
#to record the processing time

time_intervals = [50,100,150,200,250,300,350,400,450,500]
final_time=0.0
preprocessing(time_intervals,final_time)
print(word_search(sys.argv[1]))

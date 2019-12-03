 # CSC-395: Research Project by Steffie Ochoa and Lilya Woodburn
# Sources:
# * Code for October 29 class activity
# https://stackoverflow.com/questions/17038426/splitting-a-string-based-on-tab-in-the-file


import os
import glob
import re
import nltk
import string
import decimal
import math
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from decimal import Decimal
from os import listdir
from os.path import isfile, join

mypath = '../collected_tweets_october_2019'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

def get_file_names(d):
    all_files = os.listdir(d)
    return all_files

some_files = get_file_names(mypath)

#print(some_files) prints the celebrity tweet file names

#read documents
length = len(some_files)
index = 0

#while index != length:
file_index = some_files[index]
f = open(mypath + '/' + file_index, 'r')
text = f.readlines() # line 0 should say "Date  Number  Tweet"
f.close()

#cleaning
text = text[1:] # gets rid of line 0, assuming we don't need it
#print(text, '\n')
index += 1

full_text = []

for string in text:
    temp = re.split(r'\t+', string)
    temp = temp[2]
    temp = re.split(r'\n+', temp)
    temp = temp[0]
    temp = temp.lower()
    full_text.append(temp)

tf = {} # dict. of term frequencey for each word in all the tweets
tokenizer = RegexpTokenizer(r'\w+')
stop_words = set(stopwords.words('english'))
porter = PorterStemmer()
stem_word_map = {} # dict. of stemmed words and the words that stem to it
total_tweets = 0 
idf_map = {} # dict. of stemmed words and list of docs that word is in
total_words = 0

co_occurrence = {} # dict to keep word co-occurrences to build TR graph
window_size = 3

for tweet in full_text:
    total_tweets += 1
    word_tokens = tokenizer.tokenize(tweet)
    seen_words = []

    for word in word_tokens:
        if word not in stop_words:
            total_words += 1
            full_word = word # keeps the original word before stemming
            stem_word = porter.stem(word)
            
            if stem_word not in idf_map.keys():
                idf_map[stem_word] = [total_tweets]
                
            else:
                if stem_word not in seen_words:
                     idf_map[stem_word].append(total_tweets)
            
            if stem_word not in tf.keys():
                tf[stem_word] = 1
                stem_word_map[stem_word] = [[full_word, 1]]

            else:
                tf[stem_word] += 1
                found = False
                for word_list in stem_word_map[stem_word]:
                    if word_list[0] == full_word:
                        word_list[1] += 1
                        found = True
                if found == False:
                    stem_word_map[stem_word].append([full_word, 1])
            seen_words.append(stem_word)

    # begin TR co-occurrence dict building from cleaned tweet
    if len(seen_words) > 3: 
        for i in range(len(seen_words)):
            w = seen_words[i]
            
            if i == 0:
                neighbors = [seen_words[i+1], seen_words[i+2]]
            
            elif i == len(seen_words) -1:
                neighbors = [seen_words[i-1], seen_words[i-2]]
            
            else:
                neighbors = [seen_words[i-1], seen_words[i+1]]
                #print(w)
                #print('neighbors: ', neighbors)

            if w in co_occurrence.keys():
                already_neighbors = co_occurrence[w]
            
                for n in neighbors:
                
                    if n in already_neighbors.keys():
                        co_occurrence[w][n] += 1
                
                    else:
                       co_occurrence[w][n] = 1
                
            else:
                 co_occurrence[w] = {}
                
                 for n in neighbors:
                     co_occurrence[w][n] = 1
            
''' added for norm_tf (beginning, 1/2) '''
norm_tf = tf

# creates a new dictionary of normalized term frequencies
for term in norm_tf:
    norm_tf[term] /= total_words

# print(norm_tf)
''' added for norm_tf (end, 1/2) '''
        
idf_values = {}

# creates a map of idf values for each of the words
for word in idf_map.keys():
    tD = len(idf_map[word]) # how many documents the word appears in
    idf = total_tweets / tD 
    idf_values[word] = math.log(idf)
    
tf_idf = {}
results_of_tf_idf = []

# creates a new map of the tf-idf scores for each word
for word in idf_values.keys():
    tf_idf[word] = norm_tf[word] * idf_values[word]
    #print(tf_idf[word])
    #if tf_idf[word] not in results_of_tf_idf:
     #  results_of_tf_idf.append(tf_idf[word])


# Text-Rank Work
d = 0.85 # the damping factor

runs = 5 # how many times to run the algorithmn 

# initialization
old_rank = tf_idf
#print(old_rank)
new_rank = tf_idf

def neighbor_weight (word_neighbor):
    old_rank_val = old_rank[word_neighbor]
    fraction = len(co_occurrence[word_neighbor]) / sum(co_occurrence[word_neighbor].values())
    return old_rank_val * fraction

for i in range(runs): 

    for word in co_occurrence.keys():
        summation = 0
         
        for key in co_occurrence[word]: # acceses the dict attached to the word in the co-occurrance dict
             summation += neighbor_weight(key)

        new_rank[word] = (1 - d) + d * summation

    old_rank = new_rank




#print(total_words)
#print(idf_values)
#print(stem_word_map)
#print(type(full_text))
#print(tf)
#print(text)
#print(total_tweets)
#print(idf_map)
#print(results_of_tf_idf)
#print(tf_idf)
#print(len(results_of_tf_idf))
#print(co_occurrence)
print(new_rank)

'''
Thesaurus Work ---- 
        # add word as a new thesaurus key
        thesaurus = {}
        if word not in thesaurus:
            word_syns = []
            for syn in wordnet.synsets(word):
                for l in syn.lemmas():
                    # writes the lemmatized word to term_syns
                    # NOTE: bigrams are denoted by an underscore, not a space
                    word_syns.append(l.name())
            thesaurus[word] = word_syns
 '''
'''
one_percent = round(total_words * 0.01)
most_used_words = []
while 
for word in idf_values:
    if idf_values[word] > 
'''

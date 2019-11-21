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

window_size = 3

co_occurrence = {} # dict to keep word co-occurances to build TR graph

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
    
    end = 0 
    seen_words_length = len(seen_words)-1
    
    while end != seen_words_length:
        # set up new co-occurrence range of word0, word1, word2
        start = 0
        end = start + 3 # must be + 3 because sectioning is not inclusive
        sub_list = seen_words[start:end] 
        position = 0
        
        while position != 3:
            if position == 0:
                # create new dictionary entry if it doesn't exist yet
                if sub_list[0] not in co_occurrence.keys():
                    co_occurrence[sub_list[0]] = [[sub_list[1],1],
                                                  [sub_list[2],1]]

                # otherwise, determine if existing entry has sublist's values
                else:
                    found_1 = False
                    found_2 = False
                    for lists in co_occurrence[sub_list[0]]:
                        # denotes cases where word1 and/or word2 are found
                        if lists[0] == sub_list[1]:
                            lists[1] += 1
                            found_1 = True
                            
                        if lists[0] == sub_list[2]:
                            lists[1] += 1
                            found_2 = True

                    # adds word 1 or word 2 if not found        
                    if found_1 == False:
                        co_occurrence[sub_list[0]].append([sub_list[1],1])

                    if found_2 == False:
                        co_occurrence[sub_list[0]].append([sub_list[2],1])

            if position == 1:
                if sub_list[1] not in co_occurrence.keys():
                    co_occurence[sub_list[1]] = [[sub_list[0],1],
                                                 [sub_list[2],1]]
                    
                else:
                    found_0 = False
                    found_2 = False
                    for lists in co_occurrence[sub_list[0]]:
                        # denotes cases where word1 and/or word2 are found
                        if lists[0] == sub_list[0]:
                            lists[1] += 1
                            found_0 = True
                            
                        if lists[0] == sub_list[2]:
                            lists[1] += 1
                            found_2 = True

                    # adds word 1 or word 2 if not found        
                    if found_0 == False:
                        co_occurrence[sub_list[0]].append([sub_list[0],1])

                    if found_2 == False:
                        co_occurrence[sub_list[0]].append([sub_list[2],1])
        
            if position == 2:
                if sub_list[2] not in co_occurrence.keys():
                    co_occurence[sub_list[1]] = [[sub_list[0],1],
                                                 [sub_list[1],1]]
                    
                else:
                    found_0 = False
                    found_1 = False
                    for lists in co_occurrence[sub_list[0]]:
                        # denotes cases where word1 and/or word2 are found
                        if lists[0] == sub_list[0]:
                            lists[1] += 1
                            found_0 = True
                            
                        if lists[0] == sub_list[1]:
                            lists[1] += 1
                            found_1 = True

                    # adds word 1 or word 2 if not found        
                    if found_0 == False:
                        co_occurrence[sub_list[0]].append([sub_list[0],1])

                    if found_1 == False:
                        co_occurrence[sub_list[0]].append([sub_list[1],1])
        end += 1 

        
            
idf_values = {}

# creates a map of idf values for each of the words
for word in idf_map.keys():
    tD = len(idf_map[word]) # how many documents the word appears in
    idf = total_tweets / tD 
    idf_values[word] = math.log(idf)


'''            
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
#print(total_words)
#print(idf_values)
#print(stem_word_map)
#print(type(full_text))
#print(tf)
#print(text)
#print(total_tweets)
#print(idf_map)



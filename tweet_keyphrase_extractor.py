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

#read documents
length = len(some_files)
index = 0

for index in range(len(some_files)):
    print("File Name: ", some_files[index], "\n")
    file_index = some_files[index]
    f = open(mypath + '/' + file_index, 'r')
    text = f.readlines() # line 0 should say "Date  Number  Tweet"
    f.close()

    #cleaning
    text = text[1:] # gets rid of line 0, assuming we don't need it
    #print(text, '\n')
    #index += 1

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
                
    norm_tf = tf

    # creates a new dictionary of normalized term frequencies
    for term in norm_tf:
        norm_tf[term] /= total_words
            
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



    # Text-Rank Work
    d = 0.85 # the damping factor

    runs = 1000 # how many times to run the algorithmn 



    # initialization as dicts
    old_rank = tf_idf

    def total_freq_weight(n):

        local_neighbors = co_occurrence[n]
        psum = 0
        for l in local_neighbors.keys():
           psum += local_neighbors[l]

        return psum


    for i in range(runs):
        new_rank = {}

        for word in co_occurrence.keys():

            summation = 0
            #print(word)

            nws = co_occurrence[word]
            for n in nws:

                   #print(n)

                   summation += old_rank[n] * nws[n] / total_freq_weight(n)

            new_rank[word] = (1 - d) + d * summation

        old_rank = new_rank

    new_rank = old_rank 


    words_to_sort = []

    sorted_words = sorted(new_rank.items(), key=lambda kv: kv[1], reverse = True)


    # extracts the top percent of stemmed words
    percent = 0.03
    top_word_amount = round(total_words * percent)
    top_stemmed_words = []

    sorted_words_no_vals = [lst[0] for lst in sorted_words]
    top_stemmed_words = sorted_words_no_vals[:top_word_amount]    

    #print("top stemmed words: ", top_stemmed_words, "\n")

    all_top_words = []

    for w in top_stemmed_words:
        temp = stem_word_map[w]
        max_num = 0
        top_word = ""
        
        for i in temp:
            if i[1] > max_num:
                maximum = i
                top_word = i[0]

        all_top_words.append(top_word)

    print("top words: ", all_top_words, "\n")



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


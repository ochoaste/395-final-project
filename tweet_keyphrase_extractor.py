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

tf = {}

tokenizer = RegexpTokenizer(r'\w+')
stop_words = set(stopwords.words('english'))
porter = PorterStemmer()
thesaurus = {}

for tweet in full_text:
    # tokenize, stem, and perform tf
    word_tokens = tokenizer.tokenize(tweet)
    for word in word_tokens:
        if word not in stop_words:
            word = porter.stem(word)
            if word not in tf.keys():
                tf[word] = 1
            else:
                tf[word] += 1

        # add word as a new thesaurus key 
        if word not in thesaurus:
            word_syns = []
            for syn in wordnet.synsets(word):
                for l in syn.lemmas():
                    # writes the lemmatized word to term_syns
                    # NOTE: bigrams are denoted by an underscore, not a space
                    word_syns.append(l.name())
            thesaurus[word] = word_syns
    

#print(type(full_text))
print(tf)
print(thesaurus)
#print(text)

# CSC-395: Research Project by Steffie Ochoa and Lilya Woodburn
# Sources:
# * Code for October 29 class activity 


import os
import glob
import re
import nltk
import string
import decimal
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from decimal import Decimal
from os import listdir
from os.path import isfile, join

mypath = '../collected_tweets_october_2019'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

def get_file_names(d):
    all_files = os.listdir(d)
    return all_files

some_files = get_file_names(mypath)

print(some_files)

#read documents
length = len(some_files)
index = 0

while index != length:
    file_index = some_files[index]
    f = open(mypath + '/' + file_index, 'r')
    text = f.readlines() # line 0 should say "Date  Number  Tweet"
    f.close()

    #cleaning
    text = text[1:] # gets rid of line 0, assuming we don't need it
    print(text, '\n')
    index += 1


# end of while loop


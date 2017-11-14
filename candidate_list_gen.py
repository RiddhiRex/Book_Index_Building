import nltk, collections
import numpy as np
from nltk.collocations import *
from nltk.corpus import stopwords
import pandas as pd
import string

def process_text(input_text):
    '''
    Generates the candidate list by removing the stop words, spaces, punctuation marks.
    '''
    #removal of stop words
    bigram_count = 60
    words = nltk.word_tokenize(input_text)
    stop_words = set(stopwords.words("english"))
    filtered_words = []
    for w in words:
        if w not in stop_words:
            filtered_words.append(w)
    
    #Removal of space
    for w in filtered_words:
        w.replace(" ", "")

    #Removal of puncutation marks
    filtered_words = [''.join(c for c in s if c not in string.punctuation) for s in filtered_words]

    processed_word = []
    for each in filtered_words:
        if not each:
            continue
        else:
            processed_word.append(each) 
    
    bigram = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(processed_word)
    #To find frequently together occuring 2 words
    finder.apply_freq_filter(2)

    bigram_word = []
    bigram_words = finder.nbest(bigram.pmi, bigram_count)
    for each in bigram_words:
        bigram_word.append(each[0]+" "+each[1])
    word_list = []
    word_list.extend(processed_word)
    word_list.extend(bigram_word)
    return word_list

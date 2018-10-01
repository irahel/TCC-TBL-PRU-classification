import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import FreqDist
from string import punctuation
from string import digits
import re
import random
import sys
import copy

from csv_utils import Csv_utils

#Initializating
stemmer = RSLPStemmer()
csv_handler = Csv_utils()

#to remove noise
pt_stopwords = stopwords.words('portuguese')
punctuations = list(punctuation)
remove_digits = str.maketrans('', '', digits)

print("-----------------------------------------\n")
print("Initializing\n")
print("-----------------------------------------\n")
print("Initializing datas\n")
print("-----------------------------------------\n")

#Iniciar as bases
if len(sys.argv) >= 2:    
    datas = csv_handler.init_data('alldata.csv', int(sys.argv[1]))    
else:    
    datas = csv_handler.init_data('alldata.csv')    

all_sentences = []
all_words = []

##  to do
# fazer classe strings
# mudar construtor dos arquivos para aceitar classificação da frase
 
for elem in datas:
    for subelem in elem:
        for subsub in subelem:
            for word in subsub:
                if word[0] == 'twitter':
                    if word[1] == 'PRU':
                        subsub = (copy.deepcopy(subsub), 'PRU')
                    else:
                        subsub = (copy.deepcopy(subsub), 'NAO_PRU')
                    
for elem in datas:
    for subelem in elem:
        for subsub in subelem:
            print(subsub)
            print("\n")

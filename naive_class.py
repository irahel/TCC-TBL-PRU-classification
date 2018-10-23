import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import FreqDist
from string import punctuation, digits
import re, random, sys, copy

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
    datas = csv_handler.init_data_naive('alldata.csv', int(sys.argv[1]))  
else:    
    datas = csv_handler.init_data_naive('alldata.csv')    

#imprimindo base 
#for elem in datas:
#    print(elem)

#Definindo classes
classification = []

for elem in datas:
    classification.append(elem[1])

#imprimindo classificação
#for item in classification:
#    print(item)

all_sentences = []
all_words = []

#Limpar sentenca
for sentence in datas:    
    x = ""
    
    for item in sentence[0]:
        x += item + " "
            
    x = x.translate(remove_digits)
    x = re.sub(r'\W+', ' ', x)
    final_sentence = [stemmer.stem(x) for x in word_tokenize(x.lower(), 'portuguese') if x not in pt_stopwords and x not in punctuations]
    all_sentences.append(final_sentence)

#Separando todas as palavras
for sentence in all_sentences:
    for word in sentence:
        all_words.append(word)

#imprimindo sentenças
#for item in all_sentences:
#    print(item)

#imprimindo palavras
#for item in all_words:
#    print(item)

#Palavras mais frequentes
most_frequents_words = FreqDist(all_words)

#imprimindo palavras mais frenquentes
#for item in most_frequents_words:
#    print(item)

#relacao sentencas e palavras mais relevantes
all_featured_sentences = []

for x in all_sentences:
    featured_sentence = []
    for word in most_frequents_words.keys():
        if word in x:
            featured_sentence.append(1)
        else:
            featured_sentence.append(0)
    all_featured_sentences.append(featured_sentence)

#imprimindo a relaçao sentencas e palavras mais frequentes
#for item in all_featured_sentences:
#   print(item)

#Classes classificação
all_categories = ["PRU","NAO_PRU"]

all_featured_categories = []
for x in classification:
    if x == all_categories[0]:
        all_featured_categories.append(1)
    else:
        all_featured_categories.append(0)

#todas as categorias
#print(all_featured_categories)
#print(len(all_featured_categories))

#Transformando em array numpy
all_featured_sentences_numpy = np.array(all_featured_sentences)
all_featured_categories_numpy = np.array(all_featured_categories)

#Imprimindo todas categorias ne sentenças, numpy
#print (all_featured_sentences_numpy)
#print (all_featured_categories_numpy)

#TO DO
# TEST AND VALIDATION

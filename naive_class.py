#Para classificar com o Naive Bayes

import numpy as np
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize
from nltk import FreqDist
from string import punctuation, digits
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
import re, sys    
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

#Init base
if len(sys.argv) >= 2:    
    datas = csv_handler.init_data_naive('alldata.csv', int(sys.argv[1]))  
else:    
    datas = csv_handler.init_data_naive('alldata.csv')    

#Setting clss
classification = []

for elem in datas:
    classification.append(elem[1])

#Sentences and words
all_sentences = []
all_words = []

#Clean sentence
for sentence in datas:    
    x = ""
    
    for item in sentence[0]:
        x += item + " "
            
    x = x.translate(remove_digits)
    x = re.sub(r'\W+', ' ', x)
    final_sentence = [stemmer.stem(x) for x in word_tokenize(x.lower(), 'portuguese') if x not in pt_stopwords and x not in punctuations]
    all_sentences.append(final_sentence)

#Setting words
for sentence in all_sentences:
    for word in sentence:
        all_words.append(word)

#Frequents words
most_frequents_words = FreqDist(all_words)

#Featured sentences
all_featured_sentences = []
for x in all_sentences:
    featured_sentence = []
    for word in most_frequents_words.keys():
        if word in x:
            featured_sentence.append(1)
        else:
            featured_sentence.append(0)
    all_featured_sentences.append(featured_sentence)

#Class classification
all_categories = ["NAO_PRU","PRU"]
all_featured_categories = []
for x in classification:
    if x == all_categories[0]:
        all_featured_categories.append(1)
    else:
        all_featured_categories.append(0)

#Numpy arrays
all_featured_sentences_numpy = np.array(all_featured_sentences)
all_featured_categories_numpy = np.array(all_featured_categories)

#**********************************
#TEST
gnb = GaussianNB()
lr = LogisticRegression(penalty="l1")
svm = SVC(kernel='linear', C=0.5)
knn = KNeighborsClassifier(n_neighbors=5)

#TO DO
# TEST AND VALIDATION
to_test = knn


print("avaliando modelo!!")
scoresAccuracy = cross_val_score(to_test, all_featured_sentences_numpy, all_featured_categories_numpy,cv= 10, scoring='accuracy')
print("acuracia")
print(scoresAccuracy)
print(scoresAccuracy.mean())
scoresPrecision = cross_val_score(to_test, all_featured_sentences_numpy, all_featured_categories_numpy,cv= 10, scoring='precision')
print("precisao")
print(scoresPrecision)
print(scoresPrecision.mean())
scoresRecall = cross_val_score(to_test, all_featured_sentences_numpy, all_featured_categories_numpy,cv= 10, scoring='recall')
print("recall")
print(scoresRecall)
print(scoresRecall.mean())
y_predict = cross_val_predict(to_test, all_featured_sentences_numpy, all_featured_categories_numpy)
a = confusion_matrix(all_featured_categories_numpy, y_predict)
print(a)

print("FIM")
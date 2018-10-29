import nltk.corpus
from nltk.tag import BrillTaggerTrainer, brill
import csv
import sys

from csv_utils import Csv_utils
from test_protocol import Test_protocol
from nlp_utils import Nlp_utils


print("-----------------------------------------\n")
print("Initializing\n")
print("-----------------------------------------\n")
print("Initializing datas\n")
print("-----------------------------------------\n")
#Funções implementadas
csv_handler = Csv_utils()
test_handler = Test_protocol()
nlp_handler = Nlp_utils()

#Iniciar as bases
if len(sys.argv) >= 2:    
    datas = csv_handler.init_data('alldata.csv', int(sys.argv[1]))    
else:    
    datas = csv_handler.init_data('alldata.csv')    


for item in datas:
    for sub in item:
        for subsub in sub:            
            print(subsub)



#print("--------------")
#print(type(datas))
#print(len(datas))


#tuple<list<list<list<tuple<str>>>>>

#datas = ([treino], [teste])
#datas[0][0] == datas[1][0]
#tupla de listas

#for item in datas[0][0]:
#    iterator = 0
#    while(iterator < len(item)):            
#        if(item[iterator][0] == 'twitter'):
#            print(item[iterator])
#            if(item[iterator][1] == 'PRU'):
#                print("--------------------------------------")
#        iterator += 1

#for elem in datas[1][0]:
#    for item in elem:
        #if item[0] == 'twitter':
#        print(item)
            #if(item[1] == 'PRU'):
             #   print("aaaaaaaaaaa")

if(datas != None):
    print("loaded datas OK\n")
    print("-----------------------------------------\n")    

word_patterns = [
    (r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
    (r'.*ould$', 'MD'),
    (r'.*ing$', 'VBG'),
    (r'.*ed$', 'VBD'),
    (r'.*ness$', 'NN'),
    (r'.*ment$', 'NN'),
    (r'.*ful$', 'JJ'),
    (r'.*ious$', 'JJ'),
    (r'.*ble$', 'JJ'),
    (r'.*ic$', 'JJ'),
    (r'.*ive$', 'JJ'),
    (r'.*ic$', 'JJ'),
    (r'.*est$', 'JJ'),
    (r'^a$', 'PREP'),
]

print("Initializing the train\n")
print("-----------------------------------------\n")

results = []
interator = 0
#Rodar o tbl para cada fold
while(interator < len(datas[0])):    
    raubt_tagger = nlp_handler.backoff_tagger(datas[0][interator], [nltk.tag.AffixTagger,
        nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger],
        backoff=nltk.tag.RegexpTagger(word_patterns))

    templates = brill.fntbl37()
    
    trainer = BrillTaggerTrainer(raubt_tagger, templates)
    braubt_tagger = trainer.train(datas[0][interator], max_rules=100, min_score=3)

    print("Rules and scores\n")
    print("-----------------------------------------\n")

    scores = braubt_tagger.train_stats('rulescores')
    rules = braubt_tagger.rules()
    rules_by_scores = []

    for index in range(len(scores)):
        rules_by_scores.append((scores[index], rules[index]))

    for elem in rules_by_scores:
        if 'PRU' in elem[1].__str__():
            print(elem[0], elem[1].__str__())
    
    print("-----------------------------------------\n")

    print("Train ended OK\n")
    print("-----------------------------------------\n")

    print("Evaluate the model")
    results.append(test_handler.test(braubt_tagger, datas[1][interator]))
        
    print("-----------------------------------------\n")
    #print("BRAUBT train stats: ", braubt_tagger.train_stats(), "\n")
    #print("-----------------------------------------\n")
    print("End interaction ", interator)
    interator += 1
    
#Tirar a media
#index
#0 = Accuracy
#1 = Recall pru
#2 = Recall n pru
#3 = Precision pru
#4 = Precision n pru

cross_results = [0,0,0,0,0]
for elem in results:
    cross_results[0] += elem[0]
    cross_results[1] += elem[1]
    cross_results[2] += elem[2]
    cross_results[3] += elem[3]
    cross_results[4] += elem[4]

if len(sys.argv) >= 2:
    fold_numbers = int(sys.argv[1])
    acc_cross_result                = cross_results[0] / fold_numbers
    recall_pru_cross_result         = cross_results[1] / fold_numbers
    recall_nao_pru_cross_result     = cross_results[2] / fold_numbers
    precision_pru_cross_result      = cross_results[3] / fold_numbers
    precision_nao_pru_cross_result  = cross_results[4] / fold_numbers
else:
    acc_cross_result                = cross_results[0] / 5
    recall_pru_cross_result         = cross_results[1] / 5
    recall_nao_pru_cross_result     = cross_results[2] / 5
    precision_pru_cross_result      = cross_results[3] / 5
    precision_nao_pru_cross_result  = cross_results[4] / 5


print("-----------------------------------------\n")
print("END")
print("-----------------------------------------\n")
print("Total Accuracy cross", acc_cross_result)
print("Total Recall PRU cross", recall_pru_cross_result)
print("Total Recall NAO PRU cross", recall_nao_pru_cross_result)
print("Total Precision PRU cross", precision_pru_cross_result)
print("Total Precision NAO PRU cross", precision_nao_pru_cross_result)


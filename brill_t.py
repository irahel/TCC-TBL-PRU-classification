#Bibliotecas do python
import nltk.corpus
from nltk.tag import BrillTaggerTrainer, brill
import csv
import sys

#Bibliotecas criadas
#Operações em arquivos .csv (Lê os dados e poe na estrutura)
from csv_utils import Csv_utils
#Protocolo de teste e calculo de metricas (Acuracia, Precisão e Recall)
from test_protocol import Test_protocol
#Metodos de NLP (Tagger e Ajusta a estrutura de dados para as tuplas)
from nlp_utils import Nlp_utils


print("-----------------------------------------\n")
print("Initializing\n")
print("-----------------------------------------\n")
print("Initializing datas\n")
print("-----------------------------------------\n")

#Instanciação de bibliotecas implementadas
csv_handler = Csv_utils()
test_handler = Test_protocol()
nlp_handler = Nlp_utils()

#Inicia as bases
#Esse arquivo .py é chamado por linha de comando, é opcional escolher o numero de folds a serem criados.
#O numero padrão de folds é 5
if len(sys.argv) >= 2:    
    datas = csv_handler.init_data('alldata.csv', int(sys.argv[1]))    
else:    
    datas = csv_handler.init_data('alldata.csv')    

#A partir daqui a variavel "datas" contem a planilha "alldata.csv"
#Se precisar imprimir os dados para verificar como é formada a estrutura use algo do tipo:
#
#for item in datas:
#    for sub in item:
#        for subsub in sub:            
#            print(subsub)
#
#A estrutura geral é um tupla de listas de lista de lista de tupla
#Tem linhas, cada linha contem tuplas, cada tupla contem a palavra e sua respectiva TAG
#Ele divide a base "alldata.csv" em duas listas dentro de uma tupla, uma lista para treino e outra para teste
#datas = ([treino], [teste])
#Cada lista tem o formato
#list<list<list<tuple<str>>>>

#Se precisar imprimir o tipo dos dados use:
#print(type( nome_da_estrutura ))
#Ou o tamanho da tupla/linha use:
#print(len( nome_da_estrutura ))

#Verificação se importou os dados corretamente
if(datas != None):
    print("loaded datas OK\n")
    print("-----------------------------------------\n")    

#Padroes de palavras/tags para o TBL
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
    #Treina o TBL com cada linha da variavel "datas"
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

    #Aprende e guarda as regras para proxima iteracao
    for index in range(len(scores)):
        rules_by_scores.append((scores[index], rules[index]))

    for elem in rules_by_scores:
        if 'PRU' in elem[1].__str__():
            print(elem[0], elem[1].__str__())
    
    print("-----------------------------------------\n")
    print("Train ended OK\n")
    print("-----------------------------------------\n")
    #Testa o modelo com a classe "test_protocol" e guarda na variavel "results"
    #A variavel "results" é uma lista com os resultados para cada fold
    print("Evaluate the model")
    results.append(test_handler.test(braubt_tagger, datas[1][interator]))
    print("-----------------------------------------\n")
    print("End interaction ", interator)
    interator += 1
    
#Tirar a media
#index
#0 = Accuracy
#1 = Recall pru
#2 = Recall n pru
#3 = Precision pru
#4 = Precision n pru

#Divide os resultados
cross_results = [0,0,0,0,0]
for elem in results:
    cross_results[0] += elem[0]
    cross_results[1] += elem[1]
    cross_results[2] += elem[2]
    cross_results[3] += elem[3]
    cross_results[4] += elem[4]

#Calcula o resultado individual
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

#Imprime os resultados
print("-----------------------------------------\n")
print("END")
print("-----------------------------------------\n")
#Acuracia
print("Total Accuracy cross", acc_cross_result)
#Recall para PRUS
print("Total Recall PRU cross", recall_pru_cross_result)
#Recall para NAO PRUS
print("Total Recall NAO PRU cross", recall_nao_pru_cross_result)
#Precisao para PRUS
print("Total Precision PRU cross", precision_pru_cross_result)
#Precisao para NAO PRUS
print("Total Precision NAO PRU cross", precision_nao_pru_cross_result)
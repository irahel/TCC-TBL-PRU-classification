from nltk.tag.util import untag
from itertools import chain

class Test_protocol:
   
    #Definicao de como e calculado cada metrica
    def precision(self, classification, total):
        return classification/total
    def accuracy(self, classification_1, classification_2, true_1, true_2):    
        return ((classification_1 + classification_2)/(true_1 + true_2))
    def recall(self, classification, true):
        return classification/true


    def test(self, context, gold):                
        re_tagged_sents = context.tag_sents(untag(sent) for sent in gold)

        #Variaveis para contar as ocorrencias de PRUS e NAO PRUS

        #Quantidade de sentencas classificadas como PRU pelo TBL
        my_classf_pru   = 0
        #Quantidade de sentencas classificadas como NAO PRU pelo TBL
        my_classf_npru  = 0 

        #Quantidade de sentencas classificadas CORRETAMENTE como PRU pelo TBL
        classf_pru      = 0
        #Quantidade de sentencas classificadas CORRETAMENTE como NAO PRU pelo TBL
        classf_npru     = 0

        #Quantidade de sentecas que PRUS PRESENTES na base(retiradas da base de teste)
        true_pru        = 0
        #Quantidade de sentecas que NAO PRUS PRESENTES na base (retiradas da base de teste)
        true_npru       = 0

        for interator_index_1 in range(len(re_tagged_sents)):
            for interator_index_2 in range(len(re_tagged_sents[interator_index_1])):  
                #TRUE PRU AND N PRUS
                if gold[interator_index_1][interator_index_2][0] == 'twitter':                                                           
                    if gold[interator_index_1][interator_index_2][1] == 'PRU':
                        true_pru += 1
                    elif gold[interator_index_1][interator_index_2][1] == 'NAO_PRU':                        
                        true_npru += 1

                #CORRECT CLASSIFICATION PRU AND N PRUS
                if re_tagged_sents[interator_index_1][interator_index_2][0] == 'twitter':                                                           
                    if re_tagged_sents[interator_index_1][interator_index_2][1] == 'PRU':                        
                        #print("classification pru")
                        my_classf_pru += 1                        
                        if gold[interator_index_1][interator_index_2][1] == 'PRU':
                            #print("true pru")
                            classf_pru += 1                                                           
                    elif re_tagged_sents[interator_index_1][interator_index_2][1] == 'NAO_PRU':                        
                        #print("classification nao pru")
                        my_classf_npru += 1
                        if gold[interator_index_1][interator_index_2][1] == 'NAO_PRU':
                            #print("true nao pru")
                            classf_npru += 1

        #Escreve os resultados do teste na lista "test" e retorna
        #5 length vec
        test = [self.accuracy(classf_pru, classf_npru, true_pru, true_npru)]
        test.append(self.recall(classf_pru, true_pru))
        test.append(self.recall(classf_npru, true_npru))
        test.append(self.precision(classf_pru, my_classf_pru))
        test.append(self.precision(classf_npru, my_classf_npru))
        print("-----------------------------------------\n")
        print("Test Protocol single\n")
        print("-----------------------------------------\n")
        print("accuracy:", test[0],"\n")
        print("recall PRU:", test[1] ,"\n")
        print("recall NAO PRU:", test[2] ,"\n")
        print("precision PRU: ", test[3],"\n")
        print("precision NAO PRU: ", test[4],"\n")    

        return test

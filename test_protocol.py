from nltk.tag.util import untag
from itertools import chain

class Test_protocol:
   
    def precision(self, classification, total):
        return classification/total
    
    def accuracy(self, classification_1, classification_2, true_1, true_2):    
        return ((classification_1 + classification_2)/(true_1 + true_2))

    def recall(self, classification, true):
        return classification/true

    #def f_measure(self, classification_1, classification_2, true_1, true_2, alpha=0.5):
    #    p = self.accuracy(reference, test)
    #    r = self.recall(reference, test)
    #    if p is None or r is None:
    #        return None
    #    if p == 0 or r == 0:
    #        return 0
    #    return 1.0 / (alpha / p + (1-alpha) / r)
    
    def test(self, context, gold):                
        re_tagged_sents = context.tag_sents(untag(sent) for sent in gold)
        
        #CLASSIFICATION PRU AND N PRUS
        my_classf_pru   = 0 
        my_classf_npru  = 0 
        #CORRECT CLASSIFICATION PRU AND N PRUS
        classf_pru      = 0
        classf_npru     = 0
        #TRUE PRU AND N PRUS
        true_pru        = 0
        true_npru       = 0
        
        interator_index_1 = 0
        while(interator_index_1 < len(re_tagged_sents)):
            interator_index_2 = 0
            while(interator_index_2 < len(re_tagged_sents[interator_index_1])):          
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
                            #print(re_tagged_sents[interator_index_1], "////", gold[interator_index_1])                                                 
                        #else:
                            #errou
                            #print(re_tagged_sents[interator_index_1], "////", gold[interator_index_1])                                                 
                    elif re_tagged_sents[interator_index_1][interator_index_2][1] == 'NAO_PRU':                        
                        #print("classification nao pru")
                        my_classf_npru += 1
                        if gold[interator_index_1][interator_index_2][1] == 'NAO_PRU':
                            #print("true nao pru")
                            classf_npru += 1
                            
                interator_index_2 += 1                        
            interator_index_1 += 1
            
        #print("=---------------")
        #print(classf_pru)
        #print(classf_npru)
        #print(true_pru)
        #print(true_npru)
        #gold_tokens = list(chain(*gold))
        #test_tokens = list(chain(*tagged_sents))
        
        #5 length vec
        test = []
        test.append(self.accuracy(classf_pru, classf_npru, true_pru, true_npru))
        test.append(self.recall(classf_pru, true_pru))
        test.append(self.recall(classf_npru, true_npru))
        test.append(self.precision(classf_pru, my_classf_pru))
        test.append(self.precision(classf_npru, my_classf_npru))
        #test.append(self.f_measure(classf_pru, classf_npru, true_pru, true_npru))
        print("-----------------------------------------\n")
        print("Test Protocol single\n")
        print("-----------------------------------------\n")
        print("accuracy:", test[0],"\n")
        #Preciso definir o attr intersection nos sets        
        print("recall PRU:", test[1] ,"\n")
        print("recall NAO PRU:", test[2] ,"\n")    
        print("precision PRU: ", test[3],"\n")    
        print("precision NAO PRU: ", test[4],"\n")    
        
        return test

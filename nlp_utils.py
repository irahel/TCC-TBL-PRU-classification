class Nlp_utils:
    #coloca a tag NAO_PRU em todas as ocorrencias de twitter le(list_1_index < len(data_train_folds)):
            #for item in elem:na base de treinamento
    def tag_NAO_PRU(self, data_train_folds):                                            
    
        copy_ = data_train_folds.copy()
        
        list_1_index = 0
        while(list_1_index < len(copy_)):
            #for item in elem:
            list_2_index = 0
            while(list_2_index < len(copy_[list_1_index])):
                #for sub_item in item:
                list_3_index = 0
                while(list_3_index < len(copy_[list_1_index][list_2_index])):                    
                    if(copy_[list_1_index][list_2_index][list_3_index][0] == 'twitter'):
                        copy_[list_1_index][list_2_index][list_3_index] = ('twitter', 'NAO_PRU')            
                    list_3_index += 1                                    
                list_2_index += 1                                
            list_1_index +=1            
        return copy_

#tagger
    def backoff_tagger(self, tagged_sents, tagger_classes, backoff=None):
        if not backoff:
            backoff = tagger_classes[0](tagged_sents)
            del tagger_classes[0]
    
        for cls in tagger_classes:
            tagger = cls(tagged_sents, backoff=backoff)
            backoff = tagger
    
        return backoff

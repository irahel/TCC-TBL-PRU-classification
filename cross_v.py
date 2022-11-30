from nlp_utils import Nlp_utils
import copy, random

class Cross_v:
    #Divide a base para o cross v
    def create_folds(self, folds, data):        
        random.shuffle(data)

        train_percent = 100 - (100 / folds)

        print("train percent: ", train_percent)

        data_len = len(data)
        train_number = int((data_len * (int(train_percent)/100)))
        test_number = data_len - train_number

        print("total: ", data_len)
        print("train: ", train_number)
        print("test: ", test_number)  

        data_train_folds = []
        data_test_folds = []

        #divide os dados
        created_folds = 1
        last_index = 0
        while (created_folds <= folds):        
            #print("last index", last_index)
            #print("cross ",created_folds, "  ")
            #print("train  0:",last_index," ",last_index+test_number, ": ", len(data_new))
            #print("test  ", last_index,":",last_index+test_number)
            data_train_folds.append(data[:last_index] + data[last_index+test_number:])
            data_test_folds.append(data[last_index:(last_index+test_number)])
            last_index += test_number+1
            created_folds += 1


        nlp_handler = Nlp_utils()
        #vector = nlp_handler.tag_NAO_PRU(copy.deepcopy(data_train_folds))
        vector = copy.deepcopy(data_train_folds)
        return (vector, copy.deepcopy(data_test_folds))

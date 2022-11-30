from cross_v import Cross_v
from nltk.corpus import stopwords
from string import punctuation, digits
import re
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize

class Csv_utils:
    #cria cada tupla da linha
    def create_tuple(self, str_als):
        item1 = ""
        item2 = ""
        inited = False
        half_completed = False
        sec_inited = False
        for item in str_als:
            if item == '\'':
                if not inited:
                    inited = True
                elif half_completed:
                    if not sec_inited:
                        sec_inited = True
                    else:
                        break
                else:
                    half_completed = True
            elif item not in [" ", "", "\n", ",", "(", ")", "\'"]:
                if inited and not half_completed:
                    item1 += item
                else:
                    item2 += item
        #Para testar oque esta sendo criado    
        #print("item1 " +item1)
        #print("item2 " +item2)
        return (item1, item2)

    #cria cada lista referente a linha
    def create_list(self, str_als):
        list_re = []
        initial_index = 0
        end_index = 0
        #to remove noise
        #Removedor de digitos/pontuacao/stopwords
        pt_stopwords = stopwords.words('portuguese')
        punctuations = list(punctuation)
        remove_digits = str.maketrans('', '', digits)
        stemmer = RSLPStemmer()

        for atual, item in enumerate(str_als):
            if item == '(':
                initial_index = atual
            elif item == ')':
                tuple_analize = self.create_tuple(str_als[initial_index:atual])
                if tuple_analize[0] != "twitter":
                    x = tuple_analize[0]
                    x = x.translate(remove_digits)
                    x = re.sub(r'\W+', ' ', x)
                    final_sentence = [stemmer.stem(x) for x in word_tokenize(x.lower(), 'portuguese') if x not in pt_stopwords and x not in punctuations]
                    antique = tuple_analize[1]
                    tuple_analize = (str(final_sentence), antique)
                list_re.append(tuple_analize)
        return list_re

    #cria cada lista referente a linha (versão naive bayes)
    def create_list_naive(self, str_als):
        is_pru = False
        list_re = []
        initial_index = 0
        end_index = 0
        for atual, item in enumerate(str_als):
            if item == '(':
                initial_index = atual
            elif item == ')':
                tuple_analize = self.create_tuple(str_als[initial_index:atual])
                if tuple_analize[0] == "twitter":
                    is_pru = (tuple_analize[1] == "PRU")
                list_re.append(tuple_analize[0])
            return_class = "PRU" if is_pru else "NAO_PRU"
        return (list_re, return_class)
     
    #inicia as bases
    def init_data(self, arch_name, folds = 5):
        data = []

        with open(arch_name, 'r') as csvfile:
            data.extend(self.create_list(row) for row in csvfile)
        cross_v_handler = Cross_v()

        return cross_v_handler.create_folds(folds, data)                        

    def init_data_naive(self, arch_name, folds = 5):
        data = []

        with open(arch_name, 'r') as csvfile:
            data.extend(self.create_list_naive(row) for row in csvfile)
        return data                                                            
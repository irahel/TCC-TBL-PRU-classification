from cross_v import Cross_v

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
                else:
                    if not half_completed:
                        half_completed = True
                    else:
                        if not sec_inited:
                            sec_inited = True
                        else:
                            break
            elif not item == " " and not item == "" and not item == "\n" and not item == "," and not item == "(" and not item == ")" and not item == "\'":
                if inited and not half_completed:
                    item1 += item
                else:
                    item2 += item        
        return (item1, item2)

    #cria cada lista referente a linha
    def create_list(self, str_als):
        list_re = []
        initial_index = 0
        end_index = 0
        atual = 0
        for item in str_als:
            if item == '(':
                initial_index = atual
            elif item == ')':
                end_index = atual
                list_re.append(self.create_tuple(str_als[initial_index:end_index]))
            atual += 1
        return list_re
       
    #inicia as bases
    def init_data(self, arch_name, folds = 5):
        data = []
                                    
        with open(arch_name, 'r') as csvfile:    
            for row in csvfile:
                data.append(self.create_list(row))
                
        cross_v_handler = Cross_v()
    
        #for item in data:
            ##for sub in item:
                #if sub[0] == 'twitter':
             #       print(sub)
        
        return cross_v_handler.create_folds(folds, data)                        
                                                                       
        

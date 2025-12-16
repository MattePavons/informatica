import random

class Mazzo :
    def __init__(self,lista_carte):
        self.__carte = lista_carte


    def mescola(self):
        return random.shuffle(self.__carte)
    
    def pesca(self):
        if self.__carte == []:
           raise IndexError("MERDAAAAAAAAAAAAAAAAAAAA")
        else:        
            return self.__carte.pop()
    


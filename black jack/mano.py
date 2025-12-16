class Mano:
    def __init__(self):
        self.__carte = []

    def aggiungi_carta(self,carta):
        self.__carte.append(carta)

    @property 
    def carte(self):
        return self.__carte
    
    def svuota(self):
        self.__carte.clear()

    def __str__(self):
        cazz = ""
        for i in self.__carte:
            cazz += str(i)
        return cazz 

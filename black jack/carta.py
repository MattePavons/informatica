class Carta :
    def __init__(self, seme: str, rango: str):
        self.__seme = seme 
        self.__rango = rango 

    @property 
    def valore(self):
        if self.__rango in ["J","K","Q"]:
            return 10
        elif self.__rango == "A":
            return 11
        else:
           return int(self.__rango)
        
    @property 
    def rango(self):
        return self.__rango 
    
    def __str__(self):
      return  f"la tua carta è {self.__rango} di {self.__seme}"


    def __repr__(self):
        return f"{self.valore} di {self.__seme}"
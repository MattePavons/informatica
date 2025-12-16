import random

class Arma:
    def __init__(self, nome, danno_min, danno_max, tipo):
        # uso le property per la validazione
        self.nome = nome
        self.danno_min = danno_min
        self.danno_max = danno_max
        self.tipo = tipo

    # property

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valore):
        if not isinstance(valore, str) or not valore.strip():
            raise ValueError("Il nome dell'arma non può essere vuoto.")
        self.__nome = valore

    @property
    def danno_min(self):
        return self.__danno_min

    @danno_min.setter
    def danno_min(self, valore):
        if not isinstance(valore, int):
            raise TypeError("danno_min deve essere un intero.")
        if valore < 1:
            raise ValueError("danno_min deve essere almeno 1.")
        self.__danno_min = valore

    @property
    def danno_max(self):
        return self.__danno_max

    @danno_max.setter
    def danno_max(self, valore):
        if not isinstance(valore, int):
            raise TypeError("danno_max deve essere un intero.")
        if hasattr(self, "_Arma__danno_min") and valore < self.__danno_min:
            raise ValueError("danno_max deve essere >= danno_min.")
        self.__danno_max = valore

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, valore):
        if valore not in ("mischia", "distanza"):
            raise ValueError("tipo deve essere 'mischia' oppure 'distanza'.")
        self.__tipo = valore

    # metodi

    def danno(self):
        # ritorna un danno casuale tra min e max
        return random.randint(self.__danno_min, self.__danno_max)

    def __str__(self):
        return f"{self.__nome} ({self.__danno_min}-{self.__danno_max} dmg)"

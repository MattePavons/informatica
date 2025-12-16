from carta import Carta
from mano import Mano
from mazzo import Mazzo

class TavoloBlackjack:
    def __init__(self,):
        self.mazzo = Mazzo(self._crea_mazzo_standard)
        self.mano_giocatore = Mano()
        self.mano_banco = Mano()
        self.mazzo.mescola()

    def _crea_mazzo_standard(self):
        mazzo = []
        semi = ["Cuori", "Quadri", "Fiori", "Picche"]
        valori = ["A", "2", "3", "4", "5", "6", "7",
                    "8", "9", "10", "J", "Q", "K"]

        for seme in semi:
            for valore in valori:
                mazzo.append(Carta(seme, valore))
        return mazzo 

    def __calcolo_punteggio(self,mano_obj):
        v = 0
        for carta in mano_obj.carte:
            v += carta.valore 
        return v 
    
    def __turno_giocatore(self):
        i = ""
        while not i in ["C","S"]:
            i=input("stai o chiami carta? scegli C o S")
        return i 
    
    def __turno_banco(self):
       pb=self.__calcolo_punteggio(self.mano_banco)
       if pb <= 16:
          self.mano_banco.append(self.mazzo.pesca())  
    
    def goca_partita(self):
        while self.__calcola_punteggio(self.mano_giocatore) < 21 and self.__calcola_punteggio(self.mano_banco) < 21 :
            if self.__turno_giocatore() == "C" :
                self.mano_giocartore.aggiungi_carta(self.mazzo.pesca())
            self.__turno_banco()




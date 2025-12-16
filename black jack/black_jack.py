from carta import Carta
from mano import Mano
from mazzo import Mazzo

class TavoloBlackjack:
    def __init__(self):
        print(">>> Inizializzazione TavoloBlackjack")

        self.mazzo = Mazzo(self._crea_mazzo_standard())
        self.mano_giocatore = Mano()
        self.mano_banco = Mano()

        print("Mazzo creato")
        print("Mano giocatore creata")
        print("Mano banco creata")

        self.mazzo.mescola()
        print("Mazzo mescolato")

    def _crea_mazzo_standard(self):
        print(">>> Creazione mazzo standard")

        mazzo = []
        semi = ["Cuori", "Quadri", "Fiori", "Picche"]
        valori = ["A", "2", "3", "4", "5", "6", "7",
                  "8", "9", "10", "J", "Q", "K"]

        for seme in semi:
            for valore in valori:
                mazzo.append(Carta(seme, valore))

        print(">>> Mazzo completo:", len(mazzo), "carte")
        return mazzo

    def __calcolo_punteggio(self, mano_obj):
        v = 0
        for carta in mano_obj.carte:
            v += carta.valore
        return v

    def __turno_giocatore(self):
        print("\n>>> Turno giocatore")
        print("Carte:", self.mano_giocatore.carte)
        print("Punteggio:", self.__calcolo_punteggio(self.mano_giocatore))

        i = ""
        while i not in ["C", "S"]:
            i = input("Chiami carta o stai? (C/S): ").upper()
        return i

    def __turno_banco(self):
        print("\n>>> Turno banco")

        pb = self.__calcolo_punteggio(self.mano_banco)
        print("Carte banco:", self.mano_banco.carte)
        print("Punteggio banco:", pb)

        if pb <= 16:
            carta = self.mazzo.pesca()
            self.mano_banco.aggiungi_carta(carta)
            print("Banco pesca:", carta)
        else:
            print("Banco sta")

    def gioca_partita(self):
        print("\n>>> Inizio partita")
        for _ in range(2):
            self.mano_giocatore.aggiungi_carta(self.mazzo.pesca())
            self.mano_banco.aggiungi_carta(self.mazzo.pesca())

        print("Carte iniziali giocatore:", self.mano_giocatore)
        print("Carte iniziali banco:", self.mano_banco)


        while (
            self.__calcolo_punteggio(self.mano_giocatore) < 21
            and self.__calcolo_punteggio(self.mano_banco) < 21
        ):
            if self.__turno_giocatore() == "C":
                carta = self.mazzo.pesca()
                self.mano_giocatore.aggiungi_carta(carta)
                print("Hai pescato:", carta)

            self.__turno_banco()

        print("\n>>> Fine partita")
        print("Punteggio giocatore:", self.__calcolo_punteggio(self.mano_giocatore))
        print("Punteggio banco:", self.__calcolo_punteggio(self.mano_banco))

def main():
    print("=== AVVIO PROGRAMMA BLACKJACK ===")

    tavolo = TavoloBlackjack()
    print("Tavolo creato")

    tavolo.gioca_partita()

    print("=== FINE PROGRAMMA ===")


if __name__ == "__main__":
    main()

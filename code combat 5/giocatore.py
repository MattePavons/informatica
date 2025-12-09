from arma import Arma
from pozione import Potion


class Giocatore:
    def __init__(self, nome, salute_max, forza, destrezza):
        # validazione parametri
        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("Il nome del giocatore non può essere vuoto.")
        if not isinstance(salute_max, int) or salute_max <= 0:
            raise ValueError("salute_max deve essere un intero > 0.")
        if not isinstance(forza, int) or forza <= 0:
            raise ValueError("forza deve essere un intero > 0.")
        if not isinstance(destrezza, int) or destrezza <= 0:
            raise ValueError("destrezza deve essere un intero > 0.")

        self.__nome = nome
        self.__salute_max = salute_max
        self.__salute = salute_max

        if not (1 <= forza <= 20):
            raise ValueError("forza deve essere tra 1 e 20.")
        if not (1 <= destrezza <= 20):
            raise ValueError("destrezza deve essere tra 1 e 20.")
        self.__forza = forza
        self.__destrezza = destrezza

        self.__arma = None
        self.__buffs = []   # (stat, amount, turns_left)
        self.__pozioni = [] # max 3

        self.__setup_pozioni_iniziali()

    # metodi privati

    def __setup_pozioni_iniziali(self):
        p1 = Potion("Healing Draught", "heal", amount=10, duration=0)
        p2 = Potion("Healing Draught", "heal", amount=10, duration=0)
        if self.__forza >= self.__destrezza:
            p3 = Potion("Ogre Tonic", "buff_str", amount=2, duration=3)
        else:
            p3 = Potion("Cat's Grace", "buff_dex", amount=2, duration=3)
        self.__pozioni = [p1, p2, p3]

    def __clamp_salute(self):
        if self.__salute < 0:
            self.__salute = 0
        if self.__salute > self.__salute_max:
            self.__salute = self.__salute_max

    def __take(self, danno):
        # applica il danno
        danno_effettivo = min(danno, self.__salute)
        self.__salute -= danno_effettivo
        self.__clamp_salute()
        return danno_effettivo

    def __calcola_danno(self):
        if self.__arma is None:
            base = 1
        else:
            base = self.__arma.danno()
            if self.__arma.tipo == "mischia":
                base += self.modificatore(self.forza_effettiva)
            else:
                base += self.modificatore(self.destrezza_effettiva)
        return max(base, 0)

    def __ha_buff_stat(self, stat):
        # True se c'è almeno un buff su quella stat
        for b in self.__buffs:
            if b[0] == stat:
                return True
        return False

    # property

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valore):
        if not isinstance(valore, str) or not valore.strip():
            raise ValueError("Il nome del giocatore non può essere vuoto.")
        self.__nome = valore

    @property
    def salute_max(self):
        return self.__salute_max

    @property
    def salute(self):
        return self.__salute

    @salute.setter
    def salute(self, valore):
        if not isinstance(valore, int):
            raise TypeError("salute deve essere un intero.")
        self.__salute = valore
        self.__clamp_salute()

    @property
    def forza(self):
        return self.__forza

    @forza.setter
    def forza(self, valore):
        if not isinstance(valore, int):
            raise TypeError("forza deve essere un intero.")
        if not (1 <= valore <= 20):
            raise ValueError("forza deve essere tra 1 e 20.")
        self.__forza = valore

    @property
    def destrezza(self):
        return self.__destrezza

    @destrezza.setter
    def destrezza(self, valore):
        if not isinstance(valore, int):
            raise TypeError("destrezza deve essere un intero.")
        if not (1 <= valore <= 20):
            raise ValueError("destrezza deve essere tra 1 e 20.")
        self.__destrezza = valore

    @property
    def arma(self):
        return self.__arma

    @arma.setter
    def arma(self, valore):
        # solo oggetti Arma o None
        if valore is not None and not isinstance(valore, Arma):
            raise TypeError("arma deve essere un'istanza di Arma o None.")
        self.__arma = valore

    @property
    def pozioni(self):
        return list(self.__pozioni)

    @pozioni.setter
    def pozioni(self, lista):
        if len(lista) > 3:
            raise ValueError("Un giocatore può avere massimo 3 pozioni.")
        for p in lista:
            if not isinstance(p, Potion):
                raise TypeError("Tutti gli oggetti in pozioni devono essere Potion.")
        self.__pozioni = list(lista)

    @property
    def forza_effettiva(self):
        bonus_totale = 0
        for buff in self.__buffs:
            stat = buff[0]
            amount = buff[1]
            if stat == "str":
                bonus_totale = bonus_totale + amount
        forza_finale = self.__forza + bonus_totale
        return forza_finale

    @property
    def destrezza_effettiva(self):
        bonus_totale = 0
        for buff in self.__buffs:
            stat = buff[0]
            amount = buff[1]
            if stat == "dex":
                bonus_totale = bonus_totale + amount
        destrezza_finale = self.__destrezza + bonus_totale
        return destrezza_finale

    # metodi pubblici

    def vivo(self):
        return self.__salute > 0

    def modificatore(self, valore):
        return (valore - 10) // 2

    def heal(self, amount):
        # cura il giocatore
        if not isinstance(amount, int):
            raise TypeError("L'ammontare della cura deve essere un intero.")
        if amount < 0:
            raise ValueError("La cura non può essere negativa.")
        salute_prima = self.__salute
        self.__salute += amount
        self.__clamp_salute()
        return self.__salute - salute_prima

    def add_buff(self, stat, amount, duration):
        if stat not in ("str", "dex"):
            raise ValueError("stat deve essere 'str' o 'dex'.")
        if amount <= 0 or duration <= 0:
            raise ValueError("amount e duration devono essere > 0.")
        self.__buffs.append((stat, amount, duration))

    def tick_buffs(self):
        nuovi_buff = []
        for stat, amount, turns in self.__buffs:
            turns -= 1
            if turns > 0:
                nuovi_buff.append((stat, amount, turns))
        self.__buffs = nuovi_buff

    def subisci(self, danno):
        # subisce danno con validazione
        if not isinstance(danno, int):
            raise TypeError("Il danno deve essere un intero.")
        if danno < 0:
            raise ValueError("Il danno non può essere negativo.")
        return self.__take(danno)

    def attacca(self, nemico):
        danno = self.__calcola_danno()
        return nemico.subisci(danno)

    def equipaggia(self, arma):
        # equipaggia un oggetto tipo Arma
        has_danno = hasattr(arma, "danno") and callable(getattr(arma, "danno"))
        has_tipo = hasattr(arma, "tipo")
        if not (has_danno and has_tipo):
            raise TypeError("Oggetto non equipaggiabile, non è un'arma valida.")
        self.arma = arma

    def use_potion(self, p):
        # usa una pozione se possibile
        if p not in self.__pozioni:
            raise ValueError("Pozione non presente nell'inventario.")

        if p.effect == "heal":
            if self.__salute == self.__salute_max:
                raise ValueError("Il bersaglio ha già gli HP al massimo.")
        elif p.effect == "buff_str":
            if self.__ha_buff_stat("str"):
                raise ValueError("Buff alla forza già attivo.")
        elif p.effect == "buff_dex":
            if self.__ha_buff_stat("dex"):
                raise ValueError("Buff alla destrezza già attivo.")

        log = p.apply_to(self)
        self.__pozioni.remove(p)
        return log

    def should_use_potion(self, nemico):
        # strategia semplice per uso pozioni
        if not self.__pozioni:
            return None

        hp_ratio = self.__salute / self.__salute_max

        if hp_ratio <= 0.3:
            for p in self.__pozioni:
                if p.effect == "heal":
                    return p

        if not self.__buffs:
            main_stat = "str" if self.__forza >= self.__destrezza else "dex"
            for p in self.__pozioni:
                if main_stat == "str" and p.effect == "buff_str":
                    return p
                if main_stat == "dex" and p.effect == "buff_dex":
                    return p

        return None

    def __str__(self):
        return f"{self.__nome} (HP: {self.__salute}/{self.__salute_max})"

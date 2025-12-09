class Potion:
    def __init__(self, name, effect, amount, duration=0):
        self.name = name
        self.effect = effect       
        self.amount = amount      
        self.duration = duration   
        self.__consumed = False

    #  PROPERTY 

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Il nome della pozione non può essere vuoto.")
        self.__name = value

    @property
    def effect(self):
        return self.__effect

    @effect.setter
    def effect(self, value):
        if value not in ("heal", "buff_str", "buff_dex"):
            raise ValueError("effect deve essere 'heal', 'buff_str' o 'buff_dex'.")
        self.__effect = value

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, value):
        if not isinstance(value, int):
            raise TypeError("amount deve essere un intero.")
        if value < 1:
            raise ValueError("amount deve essere >= 1.")
        self.__amount = value

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        if not isinstance(value, int):
            raise TypeError("duration deve essere un intero.")
        if value < 0:
            raise ValueError("duration deve essere >= 0.")
        self.__duration = value

    #  METODI PRIVATI 

    def __apply_heal(self, target):
        healed = target.heal(self.__amount)
        self.__consumed = True
        return healed

    def __apply_buff(self, target, stat):
        target.add_buff(stat, self.__amount, self.__duration)
        self.__consumed = True
        return self.__amount

    #  METODO PUBBLICO PRINCIPALE 

    def apply_to(self, target):
        """
        Applica l'effetto al target usando duck typing.
        Richiede:
        - heal(amount:int)->int per 'heal'
        - add_buff(stat,amount,duration)->None per buff
        Solleva:
        - ValueError se la pozione è già consumata.
        - TypeError se il target non espone i metodi richiesti.
        """
        if self.__consumed:
            raise ValueError("Pozione già consumata.")

        has_heal = hasattr(target, "heal") and callable(getattr(target, "heal"))
        has_add_buff = hasattr(target, "add_buff") and callable(getattr(target, "add_buff"))

        if self.__effect == "heal":
            if not has_heal:
                raise TypeError("Target non supporta heal().")
            healed = self.__apply_heal(target)
            return {"effect": "heal", "amount": healed, "duration": 0}

        # buff_str / buff_dex
        if not has_add_buff:
            raise TypeError("Target non supporta add_buff().")

        if self.__effect == "buff_str":
            self.__apply_buff(target, "str")
            return {"effect": "buff_str", "amount": self.__amount, "duration": self.__duration}
        elif self.__effect == "buff_dex":
            self.__apply_buff(target, "dex")
            return {"effect": "buff_dex", "amount": self.__amount, "duration": self.__duration}

        # non dovrebbe mai arrivare qui
        raise ValueError("Effetto di pozione sconosciuto.")

    def __str__(self):
        if self.__effect == "heal":
            return f"Potion({self.__name}: heal +{self.__amount})"
        else:
            return f"Potion({self.__name}: {self.__effect} +{self.__amount} x{self.__duration}t)"

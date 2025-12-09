from random import randint
from arma import Arma
from giocatore import Giocatore
from view import ConsoleView
from controller import GameController

def main():
    view = ConsoleView()

    try:
        g1 = Giocatore(
            "Pavons",
            salute_max=randint(40, 60),
            forza=randint(1, 20),
            destrezza=randint(1, 20),
        )
        g2 = Giocatore(
            "Gutaa",
            salute_max=randint(40, 60),
            forza=randint(1, 20),
            destrezza=randint(1, 20),
        )
    except (ValueError, TypeError) as e:
        view.show_validation_error("Giocatore", str(e))
        return

    try:
        if g1.forza >= g1.destrezza:
            a1 = Arma("Spada a due mani", 8, 15, "mischia")
        else:
            a1 = Arma("Arco lungo", 5, 12, "distanza")

        if g2.forza >= g2.destrezza:
            a2 = Arma("Spada a due mani", 8, 15, "mischia")
        else:
            a2 = Arma("Balestra", 8, 13, "distanza")

        g1.equipaggia(a1)
        g2.equipaggia(a2)

    except ValueError as e:
        view.show_validation_error("Arma/Equip", str(e))
        g1.arma = None
        g2.arma = None
        view.show_default_weapon(g1.nome, "attacco a mani nude")
        view.show_default_weapon(g2.nome, "attacco a mani nude")
    except TypeError as e:
        view.show_validation_error("Arma/Equip", str(e))
        g1.arma = None
        g2.arma = None
        view.show_default_weapon(g1.nome, "attacco a mani nude")
        view.show_default_weapon(g2.nome, "attacco a mani nude")

    controller = GameController(view, g1, g2)
    controller.start_game_loop()

if __name__ == "__main__":
    main()

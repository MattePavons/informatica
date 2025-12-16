from random import randint
from giocatore import Giocatore
from arma import Arma


def main() -> None:
    print("TEST CREAZIONE ARMA NON VALIDA ")
    try:
        arma_rotta = Arma("Spada Rotta", 10, 5, "mischia")  # max < min → errore
    except ValueError as e:
        print(f"[ERRORE DI VALORE] Creazione arma fallita: {e}")
    print()

    print(" SIMULAZIONE COMBATTIMENTO \n")

    # Creazione personaggi
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
    except ValueError as e:
        print(f"[ERRORE DI VALORE] Creazione giocatori fallita: {e}")
        return
    except TypeError as e:
        print(f"[ERRORE DI TIPO] Creazione giocatori fallita: {e}")
        return

    print(f"{g1.nome}: Forza={g1.forza}, Destrezza={g1.destrezza}")
    print(f"{g2.nome}: Forza={g2.forza}, Destrezza={g2.destrezza}\n")

    # Assegnazione armi
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
        print(f"[ERRORE DI VALORE] Equipaggiamento armi fallito: {e}")
        print("I giocatori combatteranno a mani nude.\n")

    except TypeError as e:
        print(f"[ERRORE DI TIPO] Equipaggiamento armi fallito: {e}")
        print("I giocatori combatteranno a mani nude.\n")

    else:
        print(f"{g1.nome} equipaggia: {a1}")
        print(f"{g2.nome} equipaggia: {a2}\n")

    print(" INIZIO COMBATTIMENTO \n")

    turno = 1
    while g1.vivo() and g2.vivo():
        print(f"--- Turno {turno} ---")

        # TURNO G1
        pozione_g1 = g1.should_use_potion(g2)
        if pozione_g1 is not None:
            try:
                log = g1.use_potion(pozione_g1)
            except ValueError as e:
                print(f"[ERRORE DI VALORE] Azione fallita ({g1.nome}, pozione): {e}")
            except TypeError as e:
                print(f"[ERRORE DI TIPO] Azione fallita ({g1.nome}, pozione): {e}")
            else:
                if log["effect"] == "heal":
                    print(f"{g1.nome} usa la pozione: {pozione_g1} e recupera {log['amount']} HP")
                else:
                    print(f"{g1.nome} usa la pozione: {pozione_g1}")

        try:
            danno1 = g1.attacca(g2)
        except ValueError as e:
            print(f"[ERRORE DI VALORE] Azione fallita ({g1.nome}, attacco): {e}")
            danno1 = 0
        except TypeError as e:
            print(f"[ERRORE DI TIPO] Azione fallita ({g1.nome}, attacco): {e}")
            danno1 = 0
        else:
            print(f"{g1.nome} attacca {g2.nome} e infligge {danno1} danni!")
        print(g2)

        if not g2.vivo():
            print()
            break

        # TURNO G2
        pozione_g2 = g2.should_use_potion(g1)
        if pozione_g2 is not None:
            try:
                log = g2.use_potion(pozione_g2)
            except ValueError as e:
                print(f"[ERRORE DI VALORE] Azione fallita ({g2.nome}, pozione): {e}")
            except TypeError as e:
                print(f"[ERRORE DI TIPO] Azione fallita ({g2.nome}, pozione): {e}")
            else:
                if log["effect"] == "heal":
                    print(f"{g2.nome} usa la pozione: {pozione_g2} e recupera {log['amount']} HP")
                else:
                    print(f"{g2.nome} usa la pozione: {pozione_g2}")

        try:
            danno2 = g2.attacca(g1)
        except ValueError as e:
            print(f"[ERRORE DI VALORE] Azione fallita ({g2.nome}, attacco): {e}")
            danno2 = 0
        except TypeError as e:
            print(f"[ERRORE DI TIPO] Azione fallita ({g2.nome}, attacco): {e}")
            danno2 = 0
        else:
            print(f"{g2.nome} attacca {g1.nome} e infligge {danno2} danni!")
        print(g1)

        # FINE ROUND: tick dei buff
        g1.tick_buffs()
        g2.tick_buffs()

        print()
        turno += 1

    print("FINE COMBATTIMENTO\n")

    if g1.vivo() and not g2.vivo():
        print(f"{g1.nome} vince il combattimento! {g1}")
    elif g2.vivo() and not g1.vivo():
        print(f"{g2.nome} vince il combattimento! {g2}")
    else:
        print("Pareggio! Entrambi sono caduti.")


if __name__ == "__main__":
    main()

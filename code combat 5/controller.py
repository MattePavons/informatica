from giocatore import Giocatore

class GameController:
    def __init__(self, view, player1, player2):
        self.view = view
        self.p1 = player1
        self.p2 = player2

    def start_game_loop(self):
        self.view.show_welcome()
        self.view.show_initial_stats(self.p1, self.p2)

        turno = 1
        while self.p1.vivo() and self.p2.vivo():
            self.view.show_turn_header(turno)
            self.handle_turn(self.p1, self.p2)
            if not self.p2.vivo():
                break
            self.handle_turn(self.p2, self.p1)
            self.p1.tick_buffs()
            self.p2.tick_buffs()
            print()
            turno += 1

        if self.p1.vivo() and not self.p2.vivo():
            self.view.show_winner(self.p1.nome)
        elif self.p2.vivo() and not self.p1.vivo():
            self.view.show_winner(self.p2.nome)
        else:
            self.view.show_winner(None)

    def handle_turn(self, attacker: Giocatore, defender: Giocatore):
        poz = attacker.should_use_potion(defender)
        if poz:
            self.view.show_potion_decision(attacker.nome, poz.name)
            try:
                log = attacker.use_potion(poz)
            except Exception as e:
                self.view.show_action_failure(attacker.nome, "pozione", str(e))
            else:
                if log["effect"] == "heal":
                    desc = f"{poz} (+{log['amount']} HP)"
                    hpmsg = str(attacker)
                else:
                    desc = str(poz)
                    hpmsg = ""
                self.view.show_potion_success(attacker.nome, desc, hpmsg)

        try:
            danno = attacker.attacca(defender)
        except Exception as e:
            self.view.show_action_failure(attacker.nome, "attacco", str(e))
            return

        # decido che stat scrivere, in modo semplice
        if attacker.arma is not None and attacker.arma.tipo == "mischia":
            eff = f"STR eff={attacker.forza_effettiva}"
        elif attacker.arma is not None:
            eff = f"DEX eff={attacker.destrezza_effettiva}"
        else:
            eff = f"STR eff={attacker.forza_effettiva}"

        self.view.show_attack_result(attacker.nome, defender.nome, danno, eff)
        print(defender)

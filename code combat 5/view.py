class ConsoleView:
    def show_welcome(self):
        print(" SIMULAZIONE COMBATTIMENTO \n")

    def show_validation_error(self, component, message):
        print(f"Errore {component}: {message}")

    def show_default_weapon(self, player_name, default_weapon_name):
        print(f"{player_name} userà {default_weapon_name}")

    def show_initial_stats(self, p1, p2):
        print("STATISTICHE INIZIALI")
        print(f"{p1.nome} HP: {p1.salute}/{p1.salute_max}, STR={p1.forza}, DEX={p1.destrezza}")
        print(f"{p2.nome} HP: {p2.salute}/{p2.salute_max}, STR={p2.forza}, DEX={p2.destrezza}\n")


    def show_turn_header(self, turn_number):
        print(f"Turno {turn_number} ")

    def show_potion_decision(self, player_name, potion_name):
        print(f"{player_name} decide di usare la pozione: {potion_name}")

    def show_action_failure(self, player_name, action_name, reason):
        print(f"{player_name} {action_name} fallita: {reason}")

    def show_potion_success(self, player_name, effect_desc, current_hp_msg):
        if current_hp_msg:
            print(f"{player_name} usa la pozione: {effect_desc} -> {current_hp_msg}")
        else:
            print(f"{player_name} usa la pozione: {effect_desc}")

    def show_attack_result(self, attacker_name, defender_name, damage, eff_stat):
        print(f"{attacker_name} attacca {defender_name} [{eff_stat}] fa {damage} danni")

    def show_winner(self, winner_name):
        if winner_name is None:
            print("Pareggio, tutti morti.")
        else:
            print(f"Vince: {winner_name}")

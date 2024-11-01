from typing import Union, Tuple, List

from app.models import Pokemon


class BattleSimulation:
    def __init__(self, type_effectiveness_service, move_handler):
        self.type_effectiveness_service = type_effectiveness_service
        self.move_handler = move_handler

    def simulate_battle(self, pokemon1: Pokemon, pokemon2: Pokemon) -> Tuple[str, List[str]]:
        battle_log = []

        while pokemon1.hp > 0 and pokemon2.hp > 0:
            damage = self.calculate_damage(pokemon1, pokemon2)
            pokemon2.hp -= damage
            battle_log.append(f"{pokemon1.name} dealt {damage} damage to {pokemon2.name}. Remaining HP: {pokemon2.hp}")
            if pokemon2.hp <= 0:
                return pokemon1.name, battle_log

            # Pokémon 2 attacks Pokémon 1
            damage = self.calculate_damage(pokemon2, pokemon1)
            pokemon1.hp -= damage
            battle_log.append(f"{pokemon2.name} dealt {damage} damage to {pokemon1.name}. Remaining HP: {pokemon1.hp}")
            if pokemon1.hp <= 0:
                return pokemon2.name, battle_log

    def calculate_damage(self, attacker: Pokemon, defender: Pokemon) -> int:
        move = self.move_handler.select_move(attacker)
        move_data = self.move_handler.get_move_data(move)
        power = move_data['power']
        type_multiplier = self.type_effectiveness_service.get_type_effectiveness(attacker.type, defender.type)

        damage = (power * attacker.attack / defender.defense) * type_multiplier
        return int(damage)

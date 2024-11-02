from typing import Tuple, List

from app.battle_logic.move_handler import MoveHandler
from app.battle_logic.type_effectiveness import TypeEffectiveness
from app.models import Pokemon


class BattleSimulation:
    def __init__(self, type_effectiveness_service: TypeEffectiveness, move_handler: MoveHandler):
        self.type_effectiveness_service = type_effectiveness_service
        self.move_handler = move_handler

    def simulate_battle(self, pokemon1: Pokemon, pokemon2: Pokemon) -> Tuple[str, List[str]]:
        """
        Simulate a battle between two Pokémon.
        :param pokemon1:
        :param pokemon2:
        :return:
        """
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

    # app/battle_logic/battle_simulation.py
    def calculate_damage(self, attacker: Pokemon, defender: Pokemon) -> int:
        """
        Calculate the damage dealt by the attacker to the defender.
        :param attacker:
        :param defender:
        :return:
        """
        move = self.move_handler.select_move(attacker)
        if not move:
            return 0

        move_data = self.move_handler.get_move_data(move)
        power = move_data['power']

        # Use move's type for type effectiveness
        move_type = [move_data['type']]
        type_multiplier = self.type_effectiveness_service.get_type_effectiveness(
            move_type,
            defender.types
        )

        # Use special attack/defense for special moves
        if move_data['damage_class'] == 'special':
            damage = (power * attacker.special_attack / defender.special_defense) * type_multiplier
        else:  # physical
            damage = (power * attacker.attack / defender.defense) * type_multiplier

        return max(1, int(damage))  # Ensure minimum 1 damage

from typing import List, Tuple

class TypeEffectiveness:
    TYPE_EFFECTIVENESS = {
        ("normal", "rock"): 0.5,
        ("normal", "ghost"): 0,
        ("normal", "steel"): 0.5,
        ("fire", "fire"): 0.5,
        ("fire", "water"): 0.5,
        ("fire", "grass"): 2.0,
        ("fire", "ice"): 2.0,
        ("fire", "bug"): 2.0,
        ("fire", "rock"): 0.5,
        ("fire", "dragon"): 0.5,
        ("fire", "steel"): 2.0
    }

    def get_type_effectiveness(self, attacker_types: List[Tuple[str]], defender_types: List[str]) -> float:
        """
        Calculate type effectiveness considering multiple types.
        Returns the product of all type effectiveness multipliers.
        """
        if not attacker_types or not defender_types:
            return 1.0

        final_effectiveness = 1.0
        for attacker_type in attacker_types:
            attacker_type_name = attacker_type[0]['name'].lower()  # Extracting type name from the tuple
            for defender_type in defender_types:
                effectiveness = self.TYPE_EFFECTIVENESS.get(
                    (attacker_type_name, defender_type.lower()),
                    1.0
                )
                final_effectiveness *= effectiveness

        return final_effectiveness

class TypeEffectiveness:
    TYPE_EFFECTIVENESS = {
        ("fire", "grass"): 2.0,
        ("grass", "water"): 2.0,
        ("water", "fire"): 2.0,
        # Add more type combinations as necessary
    }

    def get_type_effectiveness(self, attacker_type: str, defender_type: str) -> float:
        return self.TYPE_EFFECTIVENESS.get((attacker_type, defender_type), 1.0)

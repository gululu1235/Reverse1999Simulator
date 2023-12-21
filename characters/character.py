from dmg_type import DamageType

class Character:
    def __init__(self, name) -> None:
        self.name = name
        self.moxie = 0
        self.life = 0
        self.status = []
    
    def reset_current_properties(self):
        pass

    def increase_moxie(self, num):
        self.moxie = max(5, self.moxie + 1)

class Skill:
    def __init__(self, caster) -> None:
        self.type = DamageType.PHYSICAL
        self.caster = caster

    def pre_damage(self, level, battlefield) -> None:
        pass

    def get_damage_multiplier(self, level, battlefield) -> float:
        pass
    
    def post_damage(self, level, battlefield) -> None:
        pass

class Properties:
    def __init__(self) -> None:
        self.attack = 0
        self.reallity_def = 0
        self.mental_def = 0
        self.critical_rate = 0
        self.critical_resist = 0
        self.critical_dmg = 0
        self.critical_def = 0
        self.dmg_bonus = 0
        self.dmg_taken_reduction = 0
        self.incantation_might = 0
        self.ultimate_might = 0
        self.dmg_heal = 0
        self.leech_rate = 0
        self.healing_done = 0
        self.penetration_rate = 0
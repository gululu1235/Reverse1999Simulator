from characters.character import *
from characters.skill import Skill, SkillId
from status.debuffs import Weakness
from dmg_type import DamageType
from utils import first_or_default

class Centurion(Character):
    id = CharacterId.CENTURION
    def __init__(self) -> None:
        super().__init__("Centurion_330101");
        self.max_life = 9152
        self.life = 9152
        self.attack = 1720
        self.moxie = 0
        self.original_properties.reality_def = 761
        self.original_properties.mental_def = 701
        self.original_properties.critical_rate = 0.675
        self.original_properties.critical_resist = 0.1
        self.original_properties.critical_dmg = 1.801
        self.original_properties.dmg_bonus = 0.08
        self.original_properties.dmg_taken_reduction = 0.05
        self.original_properties.incantation_might = 0.18
        self.skill1 = OutdoorSuperstar(self)
        self.skill2 = VictoriousGeneral(self)
        self.ultimate = RealityShowPremier(self)
        self.reset_current_properties()
    
    def set_attacker_battle_properties(self, target): # Inheritance 1
        super().set_attacker_battle_properties(target)
        self.properties.dmg_bonus += 0.06 * self.moxie
    
    def on_moxie_change_internal(self, before, after): # Inheritance 3
        if after < before:
            heal = self.max_life * 0.2
            self.life = min(self.life + heal, self.max_life)

class OutdoorSuperstar(Skill):
    id = SkillId.OUTDOOR_SUPERSTAR
    def __init__(self, caster) -> None:
        super().__init__(caster, "OutdoorSuperstar")
        self.target_number = 2
    
    def pre_damage_internal(self, level, targets:list[Character]) -> None:
        if level == 2:
            self.caster.adjust_moxie(1)
        elif level == 3:
            self.caster.adjust_moxie(2)

    def get_skill_multiplier_internal(self, level, target:Character) -> float:
        if level == 1:
            return 1.5
        if level == 2:
            return 1.5
        elif level == 3:
            return 2.25

class VictoriousGeneral(Skill):
    id = SkillId.VICTORIOUS_GENERAL
    def __init__(self, caster) -> None:
        super().__init__(caster, "VictoriousGeneral")
        self.target_number = 1

    def get_skill_multiplier_internal(self, level, target:Character) -> float:
        if level == 1:
            return 1.8 + self.caster.moxie * 0.14
        if level == 2:
            return 2.7 + self.caster.moxie * 0.21
        elif level == 3:
            return 4.5 + self.caster.moxie * 0.35

class RealityShowPremier(Skill):
    id = SkillId.REALITY_SHOW_PREMIER
    def __init__(self, caster) -> None:
        super().__init__(caster, "RealityShowPremier")
        self.target_number = 10
        self.is_ultimate = True

    def get_skill_multiplier_internal(self, level, target:Character) -> float:
        return 3
    
    def post_damage_internal(self, level, targets:list[Character]) -> None:
        for target in targets:
            weakness = first_or_default(target.status, lambda x: isinstance(x, Weakness))
            if weakness is not None:
                weakness.adjust_times_count(1)
            else:
                target.status.append(Weakness(self, target, 1))

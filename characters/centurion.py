import copy
from characters.character import *
from status.debuffs import Weakness
from status.inheritances import CenturionInheritance
from dmg_type import DamageType

class Centurion(Character):
    def __init__(self) -> None:
        super().__init__("Centurion_330101");
        self.life = 9152
        self.attack = 1720
        self.original_properties = Properties()
        self.original_properties.reallity_def = 761
        self.original_properties.mental_def = 701
        self.original_properties.critical_rate = 0.675
        self.original_properties.critical_resist = 0.1
        self.original_properties.critical_dmg = 1.801
        self.original_properties.critical_def =0
        self.original_properties.dmg_bonus = 0.08
        self.original_properties.dmg_taken_reduction = 0.05
        self.original_properties.incantation_might = 0.18
        self.moxie = 0
        self.skill1 = OutdoorSuperstar(self)
        self.skill2 = VictoriousGeneral(self)
        self.ultimate = RealityShowPremier(self)
        self.status = [CenturionInheritance(self)]
        self.reset_current_properties()
    
    def reset_current_properties(self):
        self.properties = copy.copy(self.original_properties)
    
class OutdoorSuperstar(Skill):
    def __init__(self, caster) -> None:
        self.type = DamageType.PHYSICAL
        self.target_number = 2
        self.caster = caster
        self.name = "OutdoorSuperstar"
    
    def pre_damage(self, level, battlefield) -> None:
        if level == 2:
            self.caster.increase_moxie(1)
        elif level == 3:
            self.caster.increase_moxie(2)

    def get_damage_multiplier(self, level, battlefield) -> float:
        if level == 1:
            return 1.5
        if level == 2:
            return 1.5
        elif level == 3:
            return 2.25
    
    def post_damage(self, level, battlefield) -> None:
        pass

class VictoriousGeneral(Skill):
    def __init__(self, caster) -> None:
        self.type = DamageType.PHYSICAL
        self.target_number = 1
        self.caster = caster
        self.name = "VictoriousGeneral"
    
    def pre_damage(self, level, battlefield) -> None:
        pass

    def get_damage_multiplier(self, level, battlefield) -> float:
        if level == 1:
            return 1.8 + self.caster.moxie * 0.14
        if level == 2:
            return 2.7 + self.caster.moxie * 0.21
        elif level == 3:
            return 4.5 + self.caster.moxie * 0.35
    
    def post_damage(self, level, battlefield) -> None:
        pass

class RealityShowPremier(Skill):
    def __init__(self, caster) -> None:
        self.type = DamageType.PHYSICAL
        self.target_number = 10
        self.caster = caster
        self.name = "RealityShowPremier"
    
    def pre_damage(self, level, battlefield) -> None:
        pass

    def get_damage_multiplier(self, level, battlefield) -> float:
        return 3
    
    def post_damage(self, level, battlefield) -> None:
        for character in battlefield.Black:
            character.Status.append(Weakness(1))

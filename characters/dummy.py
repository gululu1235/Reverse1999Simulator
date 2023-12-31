import copy
from characters.character import *
from characters.skill import Skill, SkillId

class DummyCharacter(Character):
    id = CharacterId.DUMMY
    def __init__(self, name) -> None:
        super().__init__(name);
        self.attack = 100
        self.life = 8888
        self.original_properties = Properties()
        self.original_properties.reality_def = 553
        self.original_properties.mental_def = 513
        self.original_properties.critical_rate = 0
        self.original_properties.critical_resist = 0
        self.original_properties.critical_dmg = 1.3
        self.original_properties.critical_def =0.164
        self.original_properties.dmg_bonus = 0
        self.original_properties.dmg_taken_reduction = 0.14
        self.original_properties.incantation_might = 0.18
        self.original_properties.ultimate_might = 0
        self.original_properties.dmg_heal = 0
        self.original_properties.leech_rate = 0
        self.original_properties.healing_done = 0
        self.original_properties.penetration_rate = 0
        self.moxie = 0
        self.reset_current_properties()
        self.skill1 = DummySkill(self, name + "_skill1")
        self.skill2 = DummySkill(self, name + "_skill2")
    
    def reset_current_properties(self):
        self.properties = copy.copy(self.original_properties)

class DummySkill(Skill):
    id = SkillId.DUMMY
    def __init__(self, caster, name) -> None:
        super().__init__(caster, name)
        self.dealDamage = False

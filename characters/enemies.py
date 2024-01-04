from characters.character import *
from characters.skill import Skill, SkillId
from utils import random_string

class Enemy1(Character):
    id = CharacterId.ENERMY
    def __init__(self, name = None) -> None:
        if not name:
            name = "Enemy_" + random_string(5)
        super().__init__(name)
        self.attack = 1720
        self.max_life = 999999
        self.life = 999999
        self.original_properties = Properties()
        self.original_properties.reality_def = 553
        self.original_properties.mental_def = 513
        self.original_properties.critical_dmg = 1.3
        self.original_properties.critical_def =0.164
        self.original_properties.dmg_taken_reduction = 0.14
        self.original_properties.incantation_might = 0.18
        self.moxie = 0
        self.skill1 = EnemySkill1(self)
        self.skill2 = EnemySkill2(self)
        self.ultimate = EnemyUlti(self)
        self.reset_current_properties()
    
class EnemySkill1(Skill):
    id = SkillId.ENEMY_SKILL_1
    def __init__(self, caster) -> None:
        super().__init__(caster, "EnemySkill1")
        self.target_number = 1
    
    def get_skill_multiplier_internal(self, level, target:Character) -> float:
        return 0
    
class EnemySkill2(Skill):
    id = SkillId.ENEMY_SKILL_2
    def __init__(self, caster) -> None:
        super().__init__(caster, "EnemySkill2")
        self.target_number = 1
    
    def get_skill_multiplier_internal(self, level, target:Character) -> float:
        return 0

class EnemyUlti(Skill):
    id = SkillId.ENEMY_ULTI
    def __init__(self, caster) -> None:
        super().__init__(caster, "EnemyUlti")
        self.target_number = 1
        self.is_ultimate = True
    
    def get_skill_multiplier_internal(self, level, target:Character) -> float:
        return 0
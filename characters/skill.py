from enum import Enum, IntEnum
import random
from battle_info.battle_info_broker import InfoBroker
from characters.character import Character
from battle.calculation import calc_damage, calc_heal
from dmg_type import DamageType


class SkillId(IntEnum):
    INVALID = 0
    OUTDOOR_SUPERSTAR = 1
    VICTORIOUS_GENERAL = 2
    REALITY_SHOW_PREMIER = 3
    WATCH_HER_SLEEVES = 4
    PRYING_EAR = 5
    UNINVITED_REVIEWER = 6
    INHERENT_HABIT = 7
    ALCHEMY_WARE = 8
    TWENTY_SIX_SECONDARY_REACTIONS = 9
    ENEMY_SKILL_1 = 96
    ENEMY_SKILL_2 = 97
    ENEMY_ULTI = 98
    DUMMY = 99


class Skill:
    id = SkillId.INVALID
    def __init__(self, caster, name) -> None:
        self.caster = caster
        self.is_ultimate = False
        self.name = name
        self.dmgType = DamageType.PHYSICAL
        self.skillType = SkillType.ATTACK
        self.dealDamage = True
        self.heal = False
        self.target_number = 1
        self.critical_eligible = True

    def pre_damage(self, level, targets:list[Character]) -> None:
        self.pre_damage_internal(level, targets)
        InfoBroker.skill_pre_damage(self, level, targets)

    def get_skill_multiplier(self, level, target:Character) -> float:
        result = self.get_skill_multiplier_internal(level, target)
        InfoBroker.skill_get_skill_multiplier(self, level, target, result)
        return result
    
    def post_damage(self, level, targets:list[Character]) -> None:
        self.post_damage_internal(level, targets)
        InfoBroker.skill_post_damage(self, level, targets)
    
    def pre_damage_internal(self, level, targets:list[Character]) -> None:
        pass

    def get_skill_multiplier_internal(self, level, target:Character) -> float:
        return 0
    
    def post_damage_internal(self, level, targets:list[Character]) -> None:
        pass

    def execute(self, level, targets:list[Character]):
        InfoBroker.skill_execute(self, level, targets)
        self.pre_damage(level, targets)
        if self.dealDamage:
            for target in targets:
                self.caster.set_attacker_battle_properties(target)
                target.set_defender_battle_properties(self.caster)
                multiplier = self.get_skill_multiplier(level, target)
                is_crit= self.critical_eligible and is_critical(self.caster, target)
                dmg = calc_damage(self.caster, target, self.dmgType, multiplier, self.is_ultimate, is_crit, False)
                # deal damage
                dmg = min(dmg, target.life)
                target.life -= dmg
                InfoBroker.skill_deal_damage(self, level, target, dmg, is_crit)
                # update status
                target.update_status_on_damage_taken()
            self.caster.update_status_on_attack_end()
        elif self.heal:
            for target in targets:
                self.caster.set_attacker_battle_properties(target)
                multiplier = self.get_skill_multiplier(level, target)
                is_crit= self.critical_eligible and is_critical(self.caster, target)
                heal = calc_heal(self.caster, target, multiplier, is_crit)
                # heal
                heal = min(heal, target.max_life - target.life)
                target.life += heal
                InfoBroker.skill_heal(self, level, target, heal, is_crit)
                # update status
                target.update_status_on_heal_taken()
            self.caster.update_status_on_heal_end()
        if (self.is_ultimate):
            self.caster.reset_moxie()
        self.post_damage(level, targets)

class SkillType(Enum):
    BUFF = 1
    DEBUFF = 2
    ATTACK = 3
    HEAL = 4

def is_critical(attacker:Character, target:Character):
    chance = attacker.properties.critical_rate - target.properties.critical_resist
    return random.random() < chance

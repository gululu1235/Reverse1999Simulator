from enum import Enum
import random
from characters.character import Character
from calculation import calc_damage, calc_heal
from dmg_type import DamageType

class Skill:
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
        pass

    def get_skill_multiplier(self, level, target:Character) -> float:
        pass
    
    def post_damage(self, level, targets:list[Character]) -> None:
        pass

    def execute(self, level, targets:list[Character]):
        self.pre_damage(level, targets)
        if self.dealDamage:
            for target in targets:
                self.caster.set_attacker_battle_properties(target)
                target.set_defender_battle_properties(self.caster)
                multiplier = self.get_skill_multiplier(level, target)
                is_crit= self.critical_eligible and is_critical(self.caster, target)
                dmg = calc_damage(self.caster, target, self.dmgType, multiplier, self.is_ultimate, is_crit, False)
                # deal damage
                target.life = max(0, target.life - dmg)
                print("attacker:", self.caster.name, "target:", target.name, "dmg:", dmg, "life:", target.life, "critical:", is_crit)
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
                target.life = min(target.max_life, target.life + heal)
                print("healer:", self.caster.name, "target:", target.name, "heal:", heal, "life:", target.life, "critical:", is_crit)
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
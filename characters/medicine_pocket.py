from characters.character import *
from characters.skill import Skill, SkillId, SkillType
from status.buffs import Immune, Sturdiness
from status.debuffs import Daze, DmgTakenUp
from utils import first_or_default

class MedicinePocket(Character):
    id = CharacterId.MEDICINE_POCKET
    def __init__(self) -> None:
        super().__init__("MedicinePocket_301090");
        self.max_life = 9853
        self.life = 9853
        self.attack = 1539
        self.moxie = 0
        self.original_properties.reality_def = 765
        self.original_properties.mental_def = 745
        self.original_properties.critical_rate = 0.145
        self.original_properties.critical_resist = 0.14
        self.original_properties.critical_dmg = 1.473
        self.critical_def = 0.05
        self.original_properties.dmg_bonus = 0.095
        self.original_properties.dmg_taken_reduction = 0.075
        self.original_properties.healing_done_bonus = 0.18
        self.skill1 = InherentHabit(self)
        self.skill2 = AlchemyWare(self)
        self.ultimate = TwentySixSecondaryReactions(self)
        self.status = []
        self.reset_current_properties()

    def set_attacker_battle_properties(self, target): # Inheritance 3
        super().set_attacker_battle_properties(target)
        if self.life < self.max_life * 0.5:
            self.properties.healing_done_bonus += 0.1

class InherentHabit(Skill):
    id = SkillId.INHERENT_HABIT
    def __init__(self, caster) -> None:
        super().__init__(caster, "InherentHabit")
        self.target_number = 1

    def get_skill_multiplier_internal(self, level, target:Character) -> float:
        if level == 1:
            return 1.5
        elif level == 2:
            return 2.5
        elif level == 3:
            return 4.5
    
    def post_damage_internal(self, level, targets:list[Character]) -> None:
        target = targets[0]
        value = 0.2
        dmg_up = first_or_default(target.status, lambda x: isinstance(x, DmgTakenUp))
        if dmg_up is None:
            target.append_status(DmgTakenUp(self.caster, target, 1, value))
        elif dmg_up.value < value or dmg_up.turn_count < 1:
            dmg_up.value = value
            dmg_up.set_turn_count(1)

class AlchemyWare(Skill):
    id = SkillId.ALCHEMY_WARE
    def __init__(self, caster) -> None:
        super().__init__(caster, "AlchemyWare")
        self.target_number = 10
        self.skillType = SkillType.HEAL
        self.dealDamage = False
        self.heal = True

    def get_skill_multiplier_internal(self, level, target:Character) -> float:
        if level == 1:
            return 0.8
        elif level == 2:
            return 1.2
        elif level == 3:
            return 2
    
    def post_damage_internal(self, level, targets:list[Character]) -> None:
        for target in targets:
            sturdiness = first_or_default(target.status, lambda x: isinstance(x, Sturdiness))
            if sturdiness is None:
                target.status.append(Sturdiness(self, target, 1))
            else:
                sturdiness.adjust_times_count(1)

class TwentySixSecondaryReactions(Skill):
    id = SkillId.TWENTY_SIX_SECONDARY_REACTIONS
    def __init__(self, caster) -> None:
        super().__init__(caster, "TwentySixSecondaryReactions")
        self.target_number = 1
        self.is_ultimate = True
    
    def pre_damage_internal(self, level, targets:list[Character]) -> None:
        pass

    def get_skill_multiplier_internal(self, level, target:Character) -> float:
        return 4.5
    
    def post_damage_internal(self, level, targets:list[Character]) -> None:
        target = targets[0]
        daze = first_or_default(target.status, lambda x: isinstance(x, Daze))
        immune = first_or_default(target.status, lambda x: isinstance(x, Immune))
        if daze is None:
            if immune is None or not (Daze in immune.list):
                target.append_status(Daze(self.caster, target, 1))
        else:
            daze.adjust_turn_count(1)

        self.caster.adjust_moxie(1)
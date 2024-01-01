from characters.character import Character, CharacterId
from characters.skill import Skill, SkillId, SkillType
from status.buffs import Immune
from status.debuffs import DmgTakenUp, RealityDefDown, Seal
from status.status import StatusType
from utils import first_or_default

class Bkornblume(Character):
    id = CharacterId.BKORNBLUME
    def __init__(self) -> None:
        super().__init__("Bkornblume_320105");
        self.max_life = 8797
        self.life = 8797
        self.attack = 1698
        self.moxie = 0
        self.original_properties.attack_bonus_rate = 0.05
        self.original_properties.reality_def = 664
        self.original_properties.mental_def = 754
        self.original_properties.critical_rate = 0.155
        self.original_properties.critical_resist = 0.08
        self.original_properties.critical_dmg = 1.397
        self.original_properties.dmg_bonus = 0.07
        self.original_properties.dmg_taken_reduction = 0.08
        self.original_properties.ultimate_might = 0.18
        self.skill1 = WatchHerSleeves(self)
        self.skill2 = PryingEar(self)
        self.ultimate = UninvitedReviewer(self)
        self.status = []
        self.reset_current_properties()

    def set_attacker_battle_properties(self, target): # Inheritance 1
        super().set_attacker_battle_properties(target)
        if any(status.type in negStatuses for status in target.status):
            self.properties.dmg_bonus += 0.2
    
    def set_defender_battle_properties(self, attacker): # Inheritance 3
        super().set_defender_battle_properties(attacker)
        if any(status.type in negStatuses for status in attacker.status):
            self.properties.dmg_taken_reduction += 0.2

negStatuses = {StatusType.NegStatus, StatusType.Control, StatusType.StatsDown}

class WatchHerSleeves(Skill):
    id = SkillId.WATCH_HER_SLEEVES
    def __init__(self, caster) -> None:
        super().__init__(caster, "WatchHerSleeves")
        self.target_number = 2

    def get_skill_multiplier_internal(self, level, target:Character) -> float:
        enhanced = False
        if any(status.type in negStatuses for status in target.status):
            enhanced = True
        if level == 1:
            return 1.8 if enhanced else 1.35
        elif level == 2:
            return 2.65 if enhanced else 2.00
        elif level == 3:
            return 4.35 if enhanced else 3.35

class PryingEar(Skill):
    id = SkillId.PRYING_EAR
    def __init__(self, caster) -> None:
        super().__init__(caster, "PryingEar")
        self.skillType = SkillType.DEBUFF
        self.target_number = 10
        self.dealDamage = False

    def post_damage_internal(self, level, targets:list[Character]) -> None:
        value = 0
        if level == 1:
            value = 0.15
        elif level == 2:
            value = 0.2
        elif level == 3:
            value = 0.25

        for target in targets:
            dmg_up = first_or_default(target.status, lambda x: isinstance(x, DmgTakenUp))
            if dmg_up is None:
                target.append_status(DmgTakenUp(self.caster, target, 2, value))
            elif dmg_up.value < value or dmg_up.turn_count < 2:
                dmg_up.value = value
                dmg_up.set_turn_count(2)

            def_down = first_or_default(target.status, lambda x: isinstance(x, RealityDefDown))
            if def_down is None:
                target.append_status(RealityDefDown(self.caster, target, 2, value))
            elif def_down.value < value or def_down.turn_count < 2:
                def_down.value = value
                def_down.set_turn_count(2)

class UninvitedReviewer(Skill):
    id = SkillId.UNINVITED_REVIEWER
    def __init__(self, caster) -> None:
        super().__init__(caster, "UninvitedReviewer")
        self.target_number = 1
        self.is_ultimate = True

    def get_skill_multiplier_internal(self, level, target:Character) -> float:
        return 8

    def post_damage_internal(self, level, targets:list[Character]) -> None:
        for target in targets:
            seal = first_or_default(target.status, lambda x: isinstance(x, Seal))
            immune = first_or_default(target.status, lambda x: isinstance(x, Immune))
            if seal is None:
                if immune is not None and Seal in immune.list:
                    target.adjust_moxie(-2)
                else:
                    target.append_status(Seal(self.caster, target, 3))
            else:
                seal.adjust_turn_count(3)
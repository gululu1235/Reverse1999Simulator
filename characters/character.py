import copy
from enum import IntEnum
from battle_info.battle_info_broker import InfoBroker
from status.status import Status


class Character:
    def __init__(self, name) -> None:
        self.name = name
        self.moxie = 0
        self.life = 0
        self.status = []
        self.original_properties = Properties()
    
    def reset_current_properties(self):
        self.properties = copy.copy(self.original_properties)

    def adjust_moxie(self, num):
        before = self.moxie
        self.moxie = min(5, self.moxie + num)
        self.moxie = max(0, self.moxie)
        if self.moxie != before:
            self.on_moxie_change(before, self.moxie)
    
    def reset_moxie(self):
        before = self.moxie
        self.moxie = 0
        if self.moxie != before:
            self.on_moxie_change(before, self.moxie)

    def set_attacker_battle_properties(self, target):
        self.set_battle_properties()

    def set_defender_battle_properties(self, attacker):
        self.set_battle_properties()

    def set_battle_properties(self):
        self.reset_current_properties()
        for status in self.status:
            status.property_impact()
    
    def append_status(self, status:Status):
        self.status.append(status)
        InfoBroker.character_status_add(self, status)

    def update_status_on_damage_taken(self):
        for status in self.status:
            status.on_dmg_taken()
        self.evaluate_status()

    def update_status_after_use_skill(self, skill):
        for status in self.status:
            status.on_use_skill(skill)
        self.evaluate_status()

    def update_status_on_turn_start(self, own_team, opponent_team):
        for status in self.status:
            status.on_turn_start(own_team, opponent_team)
        self.evaluate_status()

    def update_status_on_turn_end(self, own_team, opponent_team):
        for status in self.status:
            status.on_turn_end(own_team, opponent_team)
        self.evaluate_status()

    def update_status_on_attack_end(self):
        for status in self.status:
            status.on_attack_end()
        self.evaluate_status()
    
    def update_status_on_heal_taken(self):
        pass

    def update_status_on_heal_end(self):
        pass
    
    def on_moxie_change(self, before, after):
        self.on_moxie_change_internal(before, after)
        InfoBroker.character_moxie_change(self, before, after)

    def on_moxie_change_internal(self, before, after):
        pass

    def evaluate_status(self):
        for status in self.status:
            if (status.times_count == 0 or status.turn_count == 0):
                self.status.remove(status)
                InfoBroker.character_status_remove(self, status)

class Properties:
    def __init__(self) -> None:
        self.attack = 0
        self.attack_bonus_rate = 0
        self.reality_def = 0
        self.reality_def_bonus_rate = 0
        self.mental_def = 0
        self.mental_def_bonus_rate = 0
        self.critical_rate = 0
        self.critical_resist = 0
        self.critical_dmg = 1.3
        self.critical_def = 0
        self.dmg_bonus = 0
        self.dmg_taken_reduction = 0
        self.incantation_might = 0
        self.ultimate_might = 0
        self.dmg_heal = 0
        self.leech_rate = 0
        self.healing_done = 0
        self.penetration_rate = 0
        self.healing_done_bonus = 0
        self.healing_taken_bonus = 0

class CharacterId(IntEnum):
    CENTURION = 1
    BKORNBLUME = 2
    MEDICINE_POCKET = 3
    ENERMY = 99
    DUMMY = 999
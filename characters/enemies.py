import copy
from characters.character import *
from status.debuffs import Weakness
from dmg_type import DamageType

class Enemy1(Character):
    def __init__(self) -> None:
        super().__init__("Enemy1");
        self.attack = 1720
        self.max_life = 999999
        self.life = 999999
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
    
    def reset_current_properties(self):
        self.properties = copy.copy(self.original_properties)
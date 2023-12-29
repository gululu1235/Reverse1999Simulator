import os
import time
from battle_info.info_processor import InfoProcessor


class BattleStatAggregator(InfoProcessor):
    def __init__(self, battlefield, output_folder):
        self.stat = {}
        self.battlefield = battlefield
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        self.filepath = output_folder + "\\battle_state_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"
        with open(self.filepath, "w") as f:
            f.write("turn,character,move_count,damage,heal\n")
        
        self.__init_stat(self.battlefield.red_team + self.battlefield.blue_team)

    def __init_stat(self, characters):
        for character in characters:
            self.stat[character.name] = {}
            self.stat[character.name]["damage"] = 0
            self.stat[character.name]["heal"] = 0
            self.stat[character.name]["move_count"] = 0

    def before_card_execute(self, card):
        if card.skill is None:
            return
        self.stat[card.skill.caster.name]["move_count"] += 1

    def skill_deal_damage(self, skill, level, target, dmg, is_crit):
        self.stat[skill.caster.name]["damage"] += dmg
    
    def skill_heal(self, skill, level, target, heal, is_crit):
        self.stat[skill.caster.name]["heal"] += heal

    def turn_end(self):
        with open(self.filepath, "a") as f:
            for character in self.stat:
                f.write(f"{self.battlefield.turn},")
                f.write(f"{character},")
                f.write(f"{self.stat[character]['move_count']},")
                f.write(f"{self.stat[character]['damage']},")
                f.write(f"{self.stat[character]['heal']}\n")
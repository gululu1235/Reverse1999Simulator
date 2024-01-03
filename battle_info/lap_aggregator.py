import os
import time
from battle_info.info_processor import InfoProcessor
import matplotlib.pyplot as plt

'''
Aggregater the output information after each battle.
Information includes:
    - character's skill count
    - character's skill dmg
    - number of bad input

'''
class LapAggregator(InfoProcessor):
    def __init__(self, output_folder):
        self.lap = -1
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        self.filepath = output_folder + "\\lap_aggregator_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"
        self.action_info = {}
        self.lap_info = {}
        self.__reset_info()
        
    def __reset_info(self):
        self.lap_info[self.lap] = {}
        self.action_info[self.lap] = {}
        self.action_info[self.lap]["bad_input"] = 0
        self.action_info[self.lap]["card_move"] = 0
        self.action_info[self.lap]["card_use"] = 0
        
    def card_move(self, card):
        self.action_info[self.lap]["card_move"] += 1
    
    def card_use(self, card):
        self.action_info[self.lap]["card_use"] += 1

    def before_card_execute(self, card):
        if card.skill is None:
            return

        if card.skill.name not in self.lap_info[self.lap]:
            self.lap_info[self.lap][card.skill.name] = {"count": 0, "dmg": 0}
        
        self.lap_info[self.lap][card.skill.name]["count"] += 1

    def skill_deal_damage(self, skill, level, target, dmg, is_crit):
        self.lap_info[self.lap][skill.name]["dmg"] += dmg
    
    def bad_input(self):
        self.action_info[self.lap]["bad_input"] += 1

    def new_lap(self, battlefield):
        self.lap += 1
        self.battlefield = battlefield
        self.__reset_info()

    def summary(self):
        unique_skills = set()
        for lap in self.lap_info.values():
            unique_skills.update(lap.keys())
        
        with open(self.filepath, "w") as f:
            f.write("lap," + ",".join(unique_skills) + ",bad_input,card_move,card_use\n")
        
        for lap in range(self.lap):
            with open(self.filepath, "a") as f:
                f.write(str(lap) + ",")
                for skill in unique_skills:
                    if skill in self.lap_info[lap]:
                        f.write(str(self.lap_info[lap][skill]["count"]) + ",")
                    else:
                        f.write("0,")
                f.write(str(self.action_info[lap]["bad_input"]) + ",")
                f.write(str(self.action_info[lap]["card_move"]) + ",")
                f.write(str(self.action_info[lap]["card_use"]) + "\n")
         
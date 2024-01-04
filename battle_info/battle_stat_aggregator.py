import os
import time
from battle_info.info_processor import InfoProcessor
import matplotlib.pyplot as plt

class BattleStatAggregator(InfoProcessor):
    def __init__(self, battlefield, output_folder):
        self.stat = {}
        self.battlefield = battlefield
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        self.filepath = output_folder + "\\battle_state_" + time.strftime("%Y%m%d-%H%M%S") + ".csv"
        with open(self.filepath, "w") as f:
            f.write("turn,color,character,move_count,damage,heal\n")
        
        self.__init_stat("red", self.battlefield.red_team.members)
        self.__init_stat("blue", self.battlefield.blue_team.members)

    def __init_stat(self, color, characters):
        for character in characters:
            self.stat[character.name] = {}
            self.stat[character.name]["color"] = color
            self.stat[character.name]["damage"] = []
            self.stat[character.name]["heal"] = []
            self.stat[character.name]["move_count"] = 0

            for _ in range(self.battlefield.max_turn + 1):
                self.stat[character.name]["damage"].append(0)
                self.stat[character.name]["heal"].append(0)

    def before_card_execute(self, card):
        if card.skill is None:
            return
        self.stat[card.skill.caster.name]["move_count"] += 1

    def skill_deal_damage(self, skill, level, target, dmg, is_crit):
        self.stat[skill.caster.name]["damage"][self.battlefield.turn] = dmg
    
    def skill_heal(self, skill, level, target, heal, is_crit):
        self.stat[skill.caster.name]["heal"][self.battlefield.turn] = heal

    def turn_end(self):
        with open(self.filepath, "a") as f:
            for character in self.stat:
                f.write(f"{self.battlefield.turn},")
                f.write(f"{self.stat[character]['color']},")
                f.write(f"{character},")
                f.write(f"{self.stat[character]['move_count']},")
                f.write(f"{sum(self.stat[character]['damage'])},")
                f.write(f"{sum(self.stat[character]['heal'])}\n")

    def battle_end(self):
        dmg_plot_file = self.filepath.replace(".csv", "_dmg.png")
        heal_plot_file = self.filepath.replace(".csv", "_heal.png")
        for character in self.stat:
            aggregated_dmg = []
            for i in range(len(self.stat[character]["damage"])):
                aggregated_dmg.append(sum(self.stat[character]["damage"][:i]))
            plt.plot(aggregated_dmg, label=character)

        plt.xlabel('Turn number')
        plt.ylabel('Total Damage')
        plt.title('Damage')
        plt.legend()
        plt.savefig(dmg_plot_file)
        plt.clf()
        for character in self.stat:
            aggregated_heal = []
            for i in range(len(self.stat[character]["heal"])):
                aggregated_heal.append(sum(self.stat[character]["heal"][:i]))
            plt.plot(aggregated_heal, label=character)

        plt.xlabel('Turn number')
        plt.ylabel('Total Heal')
        plt.title('Heal')
        plt.legend()
        plt.savefig(heal_plot_file)
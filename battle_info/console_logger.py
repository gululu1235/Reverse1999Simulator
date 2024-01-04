from battle_info.info_processor import InfoProcessor


class ConsoleLogger(InfoProcessor):
    def __init__(self, battlefield):
        self.battlefield = battlefield

    def turn_start(self):
        print('Turn:' + str(self.battlefield.turn) + ' starts.')
        print('Tune points: ' + str(self.battlefield.red_team.tune.points))
        print('Red team:')
        for character in self.battlefield.red_team.members:
            status_str = ", ".join(str(status) for status in character.status)
            status =  f"[{status_str}]"
            life_percentage = character.life / character.max_life * 100
            info = [character.name, str(character.life), f"{life_percentage:.2f}%", str(character.moxie), status]
            print("\t".join(info))
        print('Blue team:')
        for character in self.battlefield.blue_team.members:
            status_str = ", ".join(str(status) for status in character.status)
            status =  f"[{status_str}]"
            life_percentage = character.life / character.max_life * 100
            info = [character.name, str(character.life), f"{life_percentage:.2f}%", str(character.moxie), status]
            print("\t".join(info))

    def turn_end(self):
        print ('Turn' + str(self.battlefield.turn) + ' ends.')
        print ('*******************************************************')

    def before_card_execute(self, card):
        print('Executing card: ' + card.name())

    def character_status_add(self, character, status):
        pass

    def character_status_remove(self, character, status):
        pass

    def character_moxie_change(self, character, before, after):
        pass

    def skill_pre_damage(self, skill, level, targets):
        pass

    def skill_get_skill_multiplier(self, skill, level, target, multiplier):
        pass

    def skill_post_damage(self, skill, level, targets):
        pass

    def skill_execute(self, skill, level, targets):
        pass

    def skill_deal_damage(self, skill, level, target, dmg, is_crit):
        print("attacker:", skill.caster.name, "target:", target.name, "dmg:", dmg, "life:", target.life, "critical:", is_crit)

    def skill_heal(self, skill, level, target, heal, is_crit):
        print("healer:", skill.caster.name, "target:", target.name, "heal:", heal, "life:", target.life, "critical:", is_crit)

    def status_adjust_turn_count(self, status, value):
        pass

    def status_adjust_times_count(self, status, value):
        pass

    def status_set_turn_count(self, status, value):
        pass
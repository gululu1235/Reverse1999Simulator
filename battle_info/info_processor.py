class InfoProcessor:
    def __init__(self):
        pass

    def turn_start(self):
        pass

    def turn_end(self):
        pass

    def before_card_execute(self, card):
        pass

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
        pass

    def skill_heal(self, skill, level, target, heal, is_crit):
        pass

    def status_adjust_turn_count(self, status, value):
        pass

    def status_adjust_times_count(self, status, value):
        pass

    def status_set_turn_count(self, status, value):
        pass
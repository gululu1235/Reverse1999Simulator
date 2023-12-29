class BattleInfoBroker:
    def __init__(self):
        self.processors = []

    def register_processor(self, processor):
        self.processors.append(processor)
    
    def turn_start(self):
        for processor in self.processors:
            processor.turn_start()

    def turn_end(self):
        for processor in self.processors:
            processor.turn_end()

    def battle_end(self):
        for processor in self.processors:
            processor.battle_end()

    def before_card_execute(self, card):
        for processor in self.processors:
            processor.before_card_execute(card)

    def character_status_add(self, character, status):
        for processor in self.processors:
            processor.character_status_add(character, status)

    def character_status_remove(self, character, status):
        for processor in self.processors:
            processor.character_status_remove(character, status)

    def character_moxie_change(self, character, before, after):
        for processor in self.processors:
            processor.character_moxie_change(character, before, after)

    def skill_pre_damage(self, skill, level, targets):
        for processor in self.processors:
            processor.skill_pre_damage(skill, level, targets)

    def skill_get_skill_multiplier(self, skill, level, target, multiplier):
        for processor in self.processors:
            processor.skill_get_skill_multiplier(skill, level, target, multiplier)

    def skill_post_damage(self, skill, level, targets):
        for processor in self.processors:
            processor.skill_post_damage(skill, level, targets)

    def skill_execute(self, skill, level, targets):
        for processor in self.processors:
            processor.skill_execute(skill, level, targets)

    def skill_deal_damage(self, skill, level, target, dmg, is_crit):
        for processor in self.processors:
            processor.skill_deal_damage(skill, level, target, dmg, is_crit)

    def skill_heal(self, skill, level, target, heal, is_crit):
        for processor in self.processors:
            processor.skill_heal(skill, level, target, heal, is_crit)

    def status_adjust_turn_count(self, status, value):
        for processor in self.processors:
            processor.status_adjust_turn_count(status, value)

    def status_adjust_times_count(self, status, value):
        for processor in self.processors:
            processor.status_adjust_times_count(status, value)

    def status_set_turn_count(self, status, value):
        for processor in self.processors:
            processor.status_set_turn_count(status, value)

InfoBroker = BattleInfoBroker()
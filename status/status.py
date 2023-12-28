from enum import Enum

class StatusType(Enum):
    NegStatus = 1
    PosStatus = 2
    StatsDown = 3
    StatsUp = 4
    Control = 5
    Special = 6

class Status:
    def __init__(self, name, caster, target, type:StatusType, times_count = 9999, turn_count = 9999) -> None:
        self.name = name
        self.caster = caster
        self.target = target
        self.type = type
        self.times_count = times_count
        self.turn_count = turn_count

    def __str__(self):
        info = self.name
        if self.times_count < 100:
            info += '_' + str(self.times_count) + 't'
        if self.turn_count < 100:
            info += '_' + str(self.turn_count) + 'r'
        return info

    def property_impact(self):
        pass

    def on_dmg_taken(self):
        pass

    def on_turn_start(self, own_team, opponent_team):
        pass

    def on_turn_end(self, own_team, opponent_team):
        pass

    def on_attack_end(self):
        pass

    def on_use_skill(self, skill):
        pass
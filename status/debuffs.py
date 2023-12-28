from characters.character import Character
from status.status import Status, StatusType

class Weakness(Status):
    def __init__(self, caster:Character, target:Character, times_count) -> None:
        super().__init__("Weakness", caster, target, StatusType.NegStatus, times_count = times_count)

    def property_impact(self):
        if self.times_count >= 0:
            self.target.properties.dmg_bonus -= 0.25
    
    def on_attack_end(self):
        self.times_count = max(self.times_count - 1, 0)

class DmgTakenUp(Status):
    def __init__(self, caster:Character, target:Character, turn_count, value) -> None:
        super().__init__("DmgTakenUp", caster, target, StatusType.StatsDown, turn_count = turn_count)
        self.value = value

    def property_impact(self):
        self.target.properties.dmg_taken_reduction -= self.value
    
    def on_turn_end(self, own_team, opponent_team):
        self.turn_count -= 1

class RealityDefDown(Status):
    def __init__(self, caster:Character, target:Character, turn_count, value) -> None:
        super().__init__("RealityDefDown", caster, target, StatusType.StatsDown, turn_count = turn_count)
        self.value = value

    def property_impact(self):
        self.target.properties.reality_def_bonus_rate -= self.value
    
    def on_turn_end(self, own_team, opponent_team):
        self.turn_count -= 1

class Seal(Status):
    def __init__(self, caster:Character, target:Character, turn_count) -> None:
        super().__init__("Seal", caster, target, StatusType.Control, turn_count = turn_count)

    def on_turn_start(self, own_team, opponent_team):
        self.turn_count -= 1

class Daze(Status):
    def __init__(self, caster:Character, target:Character, turn_count) -> None:
        super().__init__("Daze", caster, target, StatusType.Control, turn_count = turn_count)

    def on_turn_start(self, own_team, opponent_team):
        self.turn_count -= 1
from characters.character import Character
from status.status import Status, StatusId, StatusType

class Weakness(Status):
    id = StatusId.WEAKNESS
    def __init__(self, caster:Character, target:Character, times_count) -> None:
        super().__init__("Weakness", caster, target, StatusType.NegStatus, times_count = times_count)

    def property_impact(self):
        if self.times_count >= 0:
            self.target.properties.dmg_bonus -= 0.25
    
    def on_attack_end(self):
        self.adjust_times_count(-1)

class DmgTakenUp(Status):
    id = StatusId.DMG_TAKEN_UP
    def __init__(self, caster:Character, target:Character, turn_count, value) -> None:
        super().__init__("DmgTakenUp", caster, target, StatusType.StatsDown, turn_count = turn_count)
        self.value = value

    def property_impact(self):
        self.target.properties.dmg_taken_reduction -= self.value
    
    def on_turn_end(self, own_team, opponent_team):
        self.adjust_turn_count(-1)

class RealityDefDown(Status):
    id = StatusId.REALITY_DEF_DOWN
    def __init__(self, caster:Character, target:Character, turn_count, value) -> None:
        super().__init__("RealityDefDown", caster, target, StatusType.StatsDown, turn_count = turn_count)
        self.value = value

    def property_impact(self):
        self.target.properties.reality_def_bonus_rate -= self.value
    
    def on_turn_end(self, own_team, opponent_team):
        self.adjust_turn_count(-1)

class Seal(Status):
    id = StatusId.SEAL
    def __init__(self, caster:Character, target:Character, turn_count) -> None:
        super().__init__("Seal", caster, target, StatusType.Control, turn_count = turn_count)

    def on_turn_start(self, own_team, opponent_team):
        self.adjust_turn_count(-1)

class Daze(Status):
    id = StatusId.DAZE
    def __init__(self, caster:Character, target:Character, turn_count) -> None:
        super().__init__("Daze", caster, target, StatusType.Control, turn_count = turn_count)

    def on_turn_start(self, own_team, opponent_team):
        self.adjust_turn_count(-1)
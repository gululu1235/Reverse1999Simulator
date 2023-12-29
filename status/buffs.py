from status.status import Status, StatusType


class Immune(Status):
    def __init__(self, caster, target, turn_count) -> None:
        super().__init__("Immune", caster, target, StatusType.PosStatus, turn_count = turn_count)
        self.list = []

    def on_turn_end(self, own_team, opponent_team):
        self.adjust_turn_count(-1)

class Sturdiness(Status):
    def __init__(self, caster, target, times_count) -> None:
        super().__init__("Sturdiness", caster, target, StatusType.PosStatus, times_count = times_count)

    def property_impact(self):
        if self.times_count >= 0:
            self.target.properties.dmg_taken_reduction += 0.25

    def on_dmg_taken(self):
        self.adjust_times_count(-1)
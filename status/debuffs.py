class Weakness:
    def __init__(self, times) -> None:
        self.counter = times

    def PropertyImpact(self, character):
        character.dmg_bonus -= 0.25
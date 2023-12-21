class CenturionInheritance:
    def __init__(self, character) -> None:
        self.character = character

    def PropertyImpact(self):
        self.character.properties.dmg_bonus += 0.06 * self.character.moxie
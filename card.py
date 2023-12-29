class Card:
    def __init__(self, skill, level, is_wildcard = False) -> None:
        self.skill = skill
        self.level = level
        self.is_wildcard = is_wildcard
    def name(self):
        if (self.level == 0):
            return "Move"
        if (self.is_wildcard):
            return "Wildcard" + '_' + str(self.level)
        return self.skill.name + '_' + str(self.level)
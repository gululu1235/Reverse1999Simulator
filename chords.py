from card import Card
from characters.skill import Skill


class FirstChord:
    def __init__(self, battlefield) -> None:
        self.points = 15
        self.c2_cost = 40
        self.c1 = self.refresh_cards
        self.battlefield = battlefield

    def after_move(self):
        self.points += 3
    
    def after_merge(self):
        self.points += 2
    
    def turn_start(self):
        self.points += 5
    
    def after_use_skill(self):
        self.points += 4
    
    def refresh_cards(self):
        if self.points < 25:
            raise "Not enough points"
        self.points -= 25

        cards = self.battlefield.red_card_server.get_initial_cards(self.battlefield.position_count)
        for i in range(len(self.battlefield.current_cards)):
            if not self.battlefield.current_cards[i].skill.is_ultimate:
                self.battlefield.current_cards[i].skill = cards[i].skill

    def add_wild_card(self):
        if self.points < self.c2_cost:
            raise "Not enough points"
        self.points -= self.c2_cost
        self.c2_cost = min(self.c2_cost + 10, 60)
        self.battlefield.current_cards.append(Card(Skill(None, "wildcard"), 1, True))
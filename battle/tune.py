from battle.card import Card
from battle_info.battle_info_broker import InfoBroker
from characters.skill import Skill


class FirstTune:
    def __init__(self, battlefield) -> None:
        self.points = 15
        self.c2_cost = 40
        self.c1 = self.refresh_cards
        self.battlefield = battlefield

    def after_move(self):
        self.points = min(99, self.points + 3)
    
    def after_merge(self):
        self.points = min(99, self.points + 2)
    
    def turn_start(self):
        self.points = min(99, self.points + 5)
    
    def after_use_skill(self):
        self.points = min(99, self.points + 4)
    
    def refresh_cards(self):
        if self.points < 25:
            return False
        self.points -= 25

        cards = self.battlefield.red_card_server.get_initial_cards(self.battlefield.position_count)
        for i in range(min(len(self.battlefield.current_cards), len(cards))):
            if not self.battlefield.current_cards[i].skill.is_ultimate:
                self.battlefield.current_cards[i].skill = cards[i].skill
        InfoBroker.tune_refresh_cards();
        return True

    def add_wild_card(self):
        if self.points < self.c2_cost:
            return False
        if (any(card.is_wildcard for card in self.battlefield.current_cards)):
            return False
        self.points -= self.c2_cost
        self.c2_cost = min(self.c2_cost + 10, 60)
        self.battlefield.current_cards.append(Card(Skill(None, "wildcard"), 1, True))
        InfoBroker.tune_wild_card();
        return True
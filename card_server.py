import random
import copy

class CardServer:
    def __init__(self, cardList) -> None:
        self.cardList = cardList
        self.ultimate_cards = []
    
    def reset_cards(self):
        print('Reset cards')
        self.cards = []
        for card in self.cardList:
            for _ in range(8):
                self.cards.append(copy.copy(card))

        random.shuffle(self.cards)

    def get_next(self, number):
        result = []
        while self.ultimate_cards and number > 0:
            result.append(self.ultimate_cards.pop(0))
            number -= 1

        while self.cards and number > 0:
            result.append(self.cards.pop(0))
            number -= 1
        
        if (number > 0):
            self.reset_cards()
            result = result + self.get_next(number)

        return result
    
    def get_initial_cards(self, initialCount):
        self.reset_cards()
        result = []
        randomList = self.cardList.copy()
        random.shuffle(randomList)
        if initialCount == 4:
            for _ in range(2):
                result.extend(copy.copy(card) for card in randomList)
        elif initialCount == 5 or initialCount == 7:
            result.extend(copy.copy(card) for card in randomList)
            result.append(copy.copy(randomList[0]))
        elif initialCount == 6:
            result.extend(copy.copy(card) for card in randomList)
        return result

    def check_ultimate(self, caster):
        return any(ultimate_card.skill.caster == caster for ultimate_card in self.ultimate_cards)

    def try_add_ultimate(self, card):
        caster = card.skill.caster
        if any(ultimate_card.skill.caster == caster for ultimate_card in self.ultimate_cards):
            return False
        self.ultimate_cards.append(card)
    
    def try_remove_ultimate(self, caster):
        for ultimate_card in self.ultimate_cards:
            if ultimate_card.skill.caster == caster:
                self.ultimate_cards.remove(ultimate_card)
                return True
        return False
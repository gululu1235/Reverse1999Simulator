from enum import Enum
from card_server import CardServer

class BattleFiled:
    def __init__(self, position_count, action_count, characters) -> None:
        self.position_count = position_count
        self.action_count = action_count
        card_list = []
        for character in characters:
            card_list.append(Card(character.skill1, 1))
            card_list.append(Card(character.skill2, 1))

        self.card_server = CardServer(card_list, position_count)
        self.endFlag = False
        self.turn = 0
        self.current_cards = self.card_server.getInitial()
    
    def start(self):
        self.printIntro()
        while not self.endFlag:
            self.turn += 1
            print('Turn:' + str(self.turn))
            while (len(self.current_cards) < self.position_count):
                self.current_cards.extend(self.card_server.getNext(self.position_count - len(self.current_cards)))
                self.evaluateCards()
            self.printCards()
            cards = self.getCards()
            self.executeCards(cards)
    
    def printIntro(self):
        pass

    def printCards(self):
        print('Cards:')
        print("\t".join(card.name() for card in self.current_cards))
    
    def getCards(self):
        max_count = self.action_count
        cards = []
        i = 1
        while i <= max_count:
            user_input = input("Action " + str(i) + ":")
            if user_input == 'end' or user_input.lower() == 'e':
                break
            user_inputs = user_input.split(' ')
            if user_inputs[0].lower() == 'm' and len(user_inputs) == 3:
                self.processActions((Action.Move, int(user_inputs[1]), int(user_inputs[2])))
            elif user_inputs[0].lower() == 'u' and len(user_inputs) == 2:
                cards.append(self.processActions((Action.Use, int(user_inputs[1]))))
            else:
                raise "Invalid input"

            i += 1

        return cards

    def processActions(self, action):
        result = None
        if action[0] == Action.Move:
            if action[1] == action[2]:
                return result
            picked = self.current_cards[action[1]]
            self.current_cards.insert(action[2], picked)
            if (action[2] > action[1]):
                self.current_cards.pop(action[1])
            else:
                self.current_cards.pop(action[1] + 1)
        elif action[0] == Action.Use:
            result = self.current_cards.pop(action[1])
        self.evaluateCards()
        self.printCards()
        return result

    def evaluateCards(self):
        i = 0
        run_again = False
        while i < len(self.current_cards) - 1:
            if self.current_cards[i].level == 3:
                i += 1
                continue
            if self.current_cards[i].skill.name == self.current_cards[i + 1].skill.name and self.current_cards[i].level == self.current_cards[i + 1].level:
                self.current_cards[i].level += 1
                self.current_cards.pop(i + 1)
                run_again = True
                break
            else:
                i += 1
        if run_again:
            self.evaluateCards()

    def executeCards(self, cards):
        for card in cards:
            print('Executing card: ' + card.name())


class Character:
    def __init__(self, name) -> None:
        self.skill1 = Skill(name + "_skill1")
        self.skill2 = Skill(name + "_skill2")

class Skill:
    def __init__(self, name) -> None:
        self.name = name

class Action(Enum):
    Move = 1
    Use = 2

class Card:
    def __init__(self, skill, level) -> None:
        self.skill = skill
        self.level = level
    def name(self):
        return self.skill.name + '_' + str(self.level)

battle = BattleFiled(7, 3, [Character('A'), Character('B'), Character('C')])
battle.start()
from damage_calculation import calc_damage
from enum import Enum
from card_server import CardServer
from characters.centurion import Centurion
from characters.enemies import Enemy1
from characters.dummy import *

class BattleFiled:
    def __init__(self, position_count, action_count, red_team, blue_team) -> None:
        self.position_count = position_count
        self.action_count = action_count
        self.red_team = red_team
        self.blue_team = blue_team
        card_list = []
        for character in red_team:
            card_list.append(Card(character.skill1, 1))
            card_list.append(Card(character.skill2, 1))

        self.red_card_server = CardServer(card_list, position_count)
        self.endFlag = False
        self.turn = 0
        self.current_cards = self.red_card_server.getInitial()
    
    def start(self):
        self.printIntro()
        while not self.endFlag:
            self.turn += 1
            print('Turn:' + str(self.turn))
            while (len(self.current_cards) < self.position_count):
                self.current_cards.extend(self.red_card_server.getNext(self.position_count - len(self.current_cards)))
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
                self.processActions((CardAction.Move, int(user_inputs[1]), int(user_inputs[2])))
            elif user_inputs[0].lower() == 'u' and len(user_inputs) == 2:
                cards.append(self.processActions((CardAction.Use, int(user_inputs[1]))))
            else:
                raise "Invalid input"

            i += 1

        return cards

    def processActions(self, action):
        result = None
        if action[0] == CardAction.Move:
            if action[1] == action[2]:
                return result
            picked = self.current_cards[action[1]]
            self.current_cards.insert(action[2], picked)
            if (action[2] > action[1]):
                self.current_cards.pop(action[1])
            else:
                self.current_cards.pop(action[1] + 1)
        elif action[0] == CardAction.Use:
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
                self.current_cards[i].skill.caster.increase_moxie(1)
                run_again = True
                break
            else:
                i += 1
        if run_again:
            self.evaluateCards()

    def executeCards(self, cards):
        for card in cards:
            print('Executing card: ' + card.name())
            card.skill.caster.increase_moxie(1)
            card.skill.pre_damage(card.level, self)
            for character in self.red_team:
                self.refresh_properties(character)
            for character in self.blue_team:
                self.refresh_properties(character)
            multiplier = card.skill.get_damage_multiplier(card.level, self)
            dmg = calc_damage(card.skill.caster, self.blue_team[0], card.skill.type, multiplier, False, False, False)
            self.blue_team[0].life -= dmg
            print(card.skill.caster.name, " dealt ", dmg, " damage to ", self.blue_team[0].name, " current lift: ", self.blue_team[0].life)
            card.skill.post_damage(card.level, self)

    def refresh_properties(self, character):
        character.reset_current_properties()
        for status in character.status:
            status.PropertyImpact()

class CardAction(Enum):
    Move = 1
    Use = 2

class Card:
    def __init__(self, skill, level) -> None:
        self.skill = skill
        self.level = level
    def name(self):
        return self.skill.name + '_' + str(self.level)

battle = BattleFiled(7, 3, [Centurion(), DummyCharacter('B'), DummyCharacter('C')], [Enemy1()])
battle.start()
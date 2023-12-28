import random
from characters.bkornblume import Bkornblume
from calculation import calc_damage
from enum import Enum
from card_server import CardServer
from characters.centurion import Centurion
from characters.enemies import Enemy1
from characters.dummy import *
from characters.medicine_pocket import MedicinePocket
from characters.skill import SkillType
from status.debuffs import Daze, Seal

class BattleField:
    def __init__(self, position_count, action_count, red_team, blue_team, chordType) -> None:
        self.position_count = position_count
        self.action_count = action_count
        self.red_team = red_team
        self.blue_team = blue_team
        card_list = []
        for character in red_team:
            card_list.append(Card(character.skill1, 1))
            card_list.append(Card(character.skill2, 1))

        self.red_card_server = CardServer(card_list)
        self.endFlag = False
        self.turn = 0
        self.current_cards = self.red_card_server.get_initial_cards(position_count)
        self.chord = chordType(self)
    
    def start(self):
        while not self.endFlag:
            self.turn += 1
            print('Turn:' + str(self.turn))
            while (len(self.current_cards) < self.position_count):
                self.current_cards.extend(self.red_card_server.get_next(self.position_count - len(self.current_cards)))
                self.evaluate_cards()
            self.turn_start_events()
            self.print_battlefield()
            self.print_cards()
            cards = self.get_cards_from_input()
            self.execute_cards(cards)
            self.turn_end_events()
            print('**************************************')

    def print_intro(self):
        pass

    def print_cards(self):
        print('Cards:')
        print("\t".join(card.name() for card in self.current_cards))
    
    def print_battlefield(self):
        print('Chord points: ' + str(self.chord.points))
        print('Red team:')
        for character in self.red_team:
            status_str = ", ".join(str(status) for status in character.status)
            status =  f"[{status_str}]"
            life_percentage = character.life / character.max_life * 100
            info = [character.name, str(character.life), f"{life_percentage:.2f}%", str(character.moxie), status]
            print("\t".join(info))
        print('Blue team:')
        for character in self.blue_team:
            status_str = ", ".join(str(status) for status in character.status)
            status =  f"[{status_str}]"
            life_percentage = character.life / character.max_life * 100
            info = [character.name, str(character.life), f"{life_percentage:.2f}%", str(character.moxie), status]
            print("\t".join(info))
    
    def get_cards_from_input(self):
        max_count = self.action_count
        cards = []
        def input_action_to_card(action):
            result = None
            if action[0] == CardAction.Move:
                if action[1] == action[2] or action[1] == action[2] - 1: # not moved
                    return result
                picked = self.current_cards[action[1]]
                self.current_cards.insert(action[2], picked)
                if (action[2] > action[1]):
                    self.current_cards.pop(action[1])
                else:
                    self.current_cards.pop(action[1] + 1)
                if not picked.is_wildcard:
                    result = Card(picked.skill, 0)

            elif action[0] == CardAction.Use:
                result = self.current_cards.pop(action[1])
            return result
        i = 1
        while i <= max_count:
            user_input = input("Action " + str(i) + ":")
            if user_input == 'end' or user_input.lower() == 'e':
                break
            if user_input == 'c1':
                # chord: refresh
                self.chord.refresh_cards()
                self.print_cards()
                continue
            if user_input == 'c2':
                self.chord.add_wild_card()
                self.print_cards()
                continue
            user_inputs = user_input.split(' ')
            if user_inputs[0].lower() == 'm' and len(user_inputs) == 3:
                card = input_action_to_card((CardAction.Move, int(user_inputs[1]), int(user_inputs[2])))
                if card:
                    cards.append(card)
                    i += 1
                self.evaluate_cards()
                self.print_cards()
            elif user_inputs[0].lower() == 'u' and len(user_inputs) == 2:
                cards.append(input_action_to_card((CardAction.Use, int(user_inputs[1]))))
                i += 1
                self.evaluate_cards()
                self.print_cards()
            else:
                raise "Invalid input"

        return cards

    def evaluate_cards(self):
        i = 0
        run_again = False
        while i < len(self.current_cards) - 1:
            if self.current_cards[i].level == 3:
                i += 1
                continue
            if self.current_cards[i].is_wildcard:
                if self.current_cards[i].level >= self.current_cards[i + 1].level:
                    self.current_cards[i + 1].level += 1
                    self.current_cards.pop(i)
                    run_again = True
                    break
                continue
            if self.current_cards[i].skill.name == self.current_cards[i + 1].skill.name and self.current_cards[i].level == self.current_cards[i + 1].level:
                self.current_cards[i].level += 1
                self.current_cards.pop(i + 1)
                self.current_cards[i].skill.caster.adjust_moxie(1)
                self.try_add_ultimate_card(self.current_cards[i].skill.caster)
                self.after_merge_events()
                run_again = True
                break
            else:
                i += 1
        if run_again:
            self.evaluate_cards()

    def execute_cards(self, cards):
        for card in cards:
            print('Executing card: ' + card.name())
            if (card.skill == None):
                continue

            # increase moxie
            card.skill.caster.adjust_moxie(1)

            if (card.level == 0): # move
                self.after_move_events()
                continue

            # check if caster is under control
            if self.is_under_control(card.skill.caster, card.skill):
                continue

            # find targets
            targets = random.sample(self.blue_team, min(card.skill.target_number, len(self.blue_team)))
            if card.skill.skillType == SkillType.HEAL:
                targets = random.sample(self.red_team, min(card.skill.target_number, len(self.red_team)))
            if targets:
                card.skill.execute(card.level, targets)

            self.try_add_ultimate_card(card.skill.caster)
            self.after_use_skill_events(card.skill)
    
    def is_under_control(self, character, skill):
        if any(isinstance(s, Seal) for s in character.status) and skill.is_ultimate:
            return True
        if any(isinstance(s, Daze) for s in character.status):
            return True
        return False

    def evaluate_ultimate_cards(self):
        for x in [x for x in self.current_cards if x.skill.is_ultimate]:
            if x.skill.caster.moxie < 5:
                self.red_card_server.try_remove_ultimate(x.skill.caster)
                self.current_cards.remove(x)
        for character in self.red_team:
            self.try_add_ultimate_card(character)
    
    def try_add_ultimate_card(self, character):
        if (character.moxie == 5
             and not any((card.skill.caster == character and card.skill.is_ultimate) for card in self.current_cards)
             and not self.red_card_server.check_ultimate(character)):
            self.red_card_server.try_add_ultimate(Card(character.ultimate, 1))

    def after_move_events(self):
        self.chord.after_move()

    def after_merge_events(self):
        self.chord.after_merge()

    def turn_start_events(self):
        for character in self.red_team:
            character.update_status_on_turn_start(self.red_team, self.blue_team)
        for character in self.blue_team:
            character.update_status_on_turn_start(self.blue_team, self.red_team)
        self.chord.turn_start()

    def turn_end_events(self):
        for character in self.red_team:
            character.update_status_on_turn_end(self.red_team, self.blue_team)
        for character in self.blue_team:
            character.update_status_on_turn_end(self.blue_team, self.red_team)
        self.current_cards = [x for x in self.current_cards if not x.is_wildcard]
        self.evaluate_ultimate_cards()

    def after_use_skill_events(self, skill):
        for character in self.red_team + self.blue_team:
            character.update_status_after_use_skill(skill)
        self.chord.after_use_skill()

class CardAction(Enum):
    Move = 1
    Use = 2

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


battle = BattleField(7, 3, [Centurion(), Bkornblume(), MedicinePocket()], [Enemy1()], FirstChord)
battle.start()

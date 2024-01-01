from enum import Enum
import random

from battle.card import Card
from battle.card_server import CardServer
from battle.calculation import calc_damage
from battle_info.battle_info_broker import InfoBroker
from characters.skill import SkillType
from status.debuffs import Daze, Seal


class BattleField:
    def __init__(self, position_count, action_count, red_team, blue_team, tuneType, max_turn=15) -> None:
        self.position_count = position_count
        self.action_count = action_count
        self.red_team = red_team
        self.blue_team = blue_team
        self.max_turn = max_turn
        card_list = []
        for character in red_team:
            card_list.append(Card(character.skill1, 1))
            card_list.append(Card(character.skill2, 1))

        self.red_card_server = CardServer(card_list)
        self.turn = 0
        self.current_cards = self.red_card_server.get_initial_cards(position_count)
        self.tune = tuneType(self)
        self.state = State.RUNNING
        self.turn_cards = []
        self.input_count = 0
        self.bad_input = False

    def start(self):
        self.turn_start_events()

    def step(self, input):
        if self.state == State.END:
            return self

        self.handle_input(input)
        if self.bad_input:
            return self

        if self.input_count == self.action_count:
            self.execute_cards(self.turn_cards)
            self.turn_end_events()
            self.turn_start_events()

    def handle_input(self, input):
        max_count = self.action_count
        self.bad_input = False

        # Tune cards can only be used when input_count == 0
        if self.input_count == 0 and input == 'c1':
            # tune: refresh
            if not self.tune.refresh_cards():
                self.bad_input = True
            return
        elif self.input_count == 0 and input == 'c2':
            if not self.tune.add_wild_card():
                self.bad_input = True
            return

        def input_action_to_card(action):
            result = None
            if action[0] == CardAction.Move:
                picked = self.current_cards[action[1]]
                self.current_cards.insert(action[2], picked)
                if action[2] > action[1]:
                    self.current_cards.pop(action[1])
                else:
                    self.current_cards.pop(action[1] + 1)
                if not picked.is_wildcard:
                    result = Card(picked.skill, 0)
            elif action[0] == CardAction.Use:
                result = self.current_cards.pop(action[1])
            return result

        user_inputs = input.split(' ')
        if user_inputs[0].lower() == 'm' and validate_move_input(user_inputs, self.current_cards):
            card = input_action_to_card((CardAction.Move, int(user_inputs[1]), int(user_inputs[2])))
            if card:
                self.turn_cards.append(card)
            self.evaluate_cards()
            self.input_count += 1
        elif user_inputs[0].lower() == 'u' and validate_use_input(user_inputs, self.current_cards):
            self.turn_cards.append(input_action_to_card((CardAction.Use, int(user_inputs[1]))))
            self.evaluate_cards()
            self.input_count += 1
        else:
            self.bad_input = True

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
            if (
                self.current_cards[i].skill.name == self.current_cards[i + 1].skill.name
                and self.current_cards[i].level == self.current_cards[i + 1].level
            ):
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
            InfoBroker.before_card_execute(card)
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
            self.red_card_server.try_add_ultimate(Card(character.ultimate, 4))

    def after_move_events(self):
        self.tune.after_move()

    def after_merge_events(self):
        self.tune.after_merge()

    def turn_start_events(self):
        self.turn += 1
        if self.turn > self.max_turn:
            self.state = State.END
            InfoBroker.battle_end()
            return

        self.turn_cards = []
        self.input_count = 0
        while (len(self.current_cards) < self.position_count):
            self.current_cards.extend(self.red_card_server.get_next(self.position_count - len(self.current_cards)))
            self.evaluate_cards()
        for character in self.red_team:
            character.update_status_on_turn_start(self.red_team, self.blue_team)
        for character in self.blue_team:
            character.update_status_on_turn_start(self.blue_team, self.red_team)
        self.tune.turn_start()
        InfoBroker.turn_start()

    def turn_end_events(self):
        for character in self.red_team:
            character.update_status_on_turn_end(self.red_team, self.blue_team)
        for character in self.blue_team:
            character.update_status_on_turn_end(self.blue_team, self.red_team)
        self.current_cards = [x for x in self.current_cards if not x.is_wildcard]
        self.evaluate_ultimate_cards()
        InfoBroker.turn_end()

    def after_use_skill_events(self, skill):
        for character in self.red_team + self.blue_team:
            character.update_status_after_use_skill(skill)
        self.tune.after_use_skill()

class CardAction(Enum):
    Move = 1
    Use = 2

class State(Enum):
    RUNNING = 1
    END = 2

def validate_move_input(inputs, cards):
    count = len(cards)
    if len(inputs) != 3:
        return False
    try:
        pos1 = int(inputs[1])
        pos2 = int(inputs[2])
        if pos1 < 0 or pos1 >= count or pos2 < 0 or pos2 >= count:
            return False
        if pos1 == pos2 or pos1 == pos2 - 1:
            return False
        if cards[pos1].is_wildcard and cards[pos1].level < cards[pos2].level:
            return False
    except ValueError:
        return False
    return True

def validate_use_input(inputs, cards):
    count = len(cards)
    if len(inputs) != 2:
        return False
    try:
        pos = int(inputs[1])
        if pos < 0 or pos >= count:
            return False
        if cards[pos].is_wildcard:
            return False
    except ValueError:
        return False
    return True

from enum import Enum
import random

from battle.card import Card
from battle.card_server import CardServer
from battle.calculation import calc_damage
from battle_info.battle_info_broker import InfoBroker
from characters.skill import SkillType
from status.debuffs import Daze, Seal

class Team:
    def __init__(self, position_count, action_count, members, tune_type) -> None:
        self.position_count = position_count
        self.action_count = action_count
        self.members = members
        self.tune = tune_type(self)

        card_list = []
        for character in members:
            card_list.append(Card(character.skill1, 1))
            card_list.append(Card(character.skill2, 1))
        self.card_server = CardServer(card_list)
        self.current_cards = self.card_server.get_initial_cards(position_count)
    

class BattleField:
    def __init__(self, red_position_count, red_action_count, red_team, red_tune_type,
                 blue_position_count, blue_action_count, blue_team, blue_tune_type, max_turn=15) -> None:
        
        self.red_team = Team(red_position_count, red_action_count, red_team, red_tune_type)
        self.blue_team = Team(blue_position_count, blue_action_count, blue_team, blue_tune_type)
        self.max_turn = max_turn

        self.turn = 0
        self.state = State.RUNNING
        self.turn_cards = []
        self.input_count = 0
        self.bad_input = False

        self.caster_team = self.red_team
        self.target_team = self.blue_team

    def start(self):
        self.turn_start_events()

    def step(self, input):
        if self.state == State.END:
            return self

        card, target_id = self.handle_input(input)
        if self.bad_input:
            InfoBroker.bad_input()
            return self

        if card:
            self.execute_card(card, target_id)

        if self.caster_team == self.red_team and self.input_count == self.red_team.action_count:
            self.switch_turn_events()
        elif self.caster_team == self.blue_team and self.input_count == self.blue_team.action_count:
            self.turn_end_events()
            self.turn_start_events()

    def handle_input(self, input):
        self.bad_input = False
        resolved = (None, 0)

        # Tune cards can only be used when input_count == 0
        if self.input_count == 0 and input == 'c1':
            # tune: refresh
            if not self.caster_team.tune.refresh_cards():
                self.bad_input = True
            return resolved
        elif self.input_count == 0 and input == 'c2':
            if not self.caster_team.tune.add_wild_card():
                self.bad_input = True
            return resolved

        def input_action_to_card(action):
            result = (None, 0)
            if action[0] == CardAction.Move:
                picked = self.caster_team.current_cards[action[1]]
                self.caster_team.current_cards.insert(action[2], picked)
                if action[2] > action[1]:
                    self.caster_team.current_cards.pop(action[1])
                else:
                    self.caster_team.current_cards.pop(action[1] + 1)
                if not picked.is_wildcard:
                    result = (Card(picked.skill, 0), 0)
                InfoBroker.card_move(picked)
            elif action[0] == CardAction.Use:
                result = (self.caster_team.current_cards.pop(action[1]), action[2])
                InfoBroker.card_use(result[0])
            return result

        user_inputs = input.split(' ')
        if user_inputs[0].lower() == 'm' and validate_move_input(user_inputs, self.caster_team.current_cards):
            resolved = input_action_to_card((CardAction.Move, int(user_inputs[1]), int(user_inputs[2])))
            self.evaluate_cards(self.caster_team)
            self.input_count += 1
        elif user_inputs[0].lower() == 'u' and validate_use_input(user_inputs, self.caster_team.current_cards):
            resolved = input_action_to_card((CardAction.Use, int(user_inputs[1]), int(user_inputs[2])))
            self.evaluate_cards(self.caster_team)
            self.input_count += 1
        else:
            self.bad_input = True
        
        return resolved

    def evaluate_cards(self, team):
        i = 0
        run_again = False
        cards_list = team.current_cards
        while i < len(cards_list) - 1:
            if cards_list[i].level == 3:
                i += 1
                continue
            if cards_list[i].is_wildcard:
                if cards_list[i].level >= cards_list[i + 1].level:
                    cards_list[i + 1].level += 1
                    cards_list.pop(i)
                    run_again = True
                    break
                continue
            if (
                cards_list[i].skill.name == cards_list[i + 1].skill.name
                and cards_list[i].level == cards_list[i + 1].level
            ):
                cards_list[i].level += 1
                cards_list.pop(i + 1)
                cards_list[i].skill.caster.adjust_moxie(1)
                self.try_add_ultimate_card(cards_list[i].skill.caster, team)
                self.after_merge_events(team)
                run_again = True
                break
            else:
                i += 1
        if run_again:
            self.evaluate_cards(team)

    def execute_card(self, card, target_id=0):
        InfoBroker.before_card_execute(card)
        if (card.skill == None):
            return

        # increase moxie
        card.skill.caster.adjust_moxie(1)

        if (card.level == 0): # move
            self.after_move_events(self.caster_team)
            return

        # check if caster is under control
        if self.is_under_control(card.skill.caster, card.skill):
            return

        # find targets
        def find_targets(members):
            if target_id < len(members):
                main_target = members[target_id]
            else:
                main_target = members[0]
            targets = [main_target]
            other_target_number = min(card.skill.target_number - 1, len(members) - 1)
            other_members = [x for x in members if x != main_target]
            targets.extend(random.sample(other_members, other_target_number))
            return targets

        if card.skill.skillType == SkillType.HEAL:
            targets = find_targets(self.caster_team.members)
        else:
            targets = find_targets(self.target_team.members)

        if targets:
            card.skill.execute(card.level, targets)

        self.try_add_ultimate_card(card.skill.caster, self.caster_team)
        self.after_use_skill_events(card.skill)
    
    def is_under_control(self, character, skill):
        if any(isinstance(s, Seal) for s in character.status) and skill.is_ultimate:
            return True
        if any(isinstance(s, Daze) for s in character.status):
            return True
        return False

    def evaluate_ultimate_cards(self):
        for x in [x for x in self.red_team.current_cards if x.skill.is_ultimate]:
            if x.skill.caster.moxie < 5:
                self.red_team.card_server.try_remove_ultimate(x.skill.caster)
                self.red_team.current_cards.remove(x)
        
        for x in [x for x in self.blue_team.current_cards if x.skill.is_ultimate]:
            if x.skill.caster.moxie < 5:
                self.blue_team.card_server.try_remove_ultimate(x.skill.caster)
                self.blue_team.current_cards.remove(x)

        for character in self.red_team.members:
            self.try_add_ultimate_card(character, self.red_team)
        
        for character in self.blue_team.members:
            self.try_add_ultimate_card(character, self.blue_team)
    
    def try_add_ultimate_card(self, character, team):
        if (character.moxie == 5
             and not any((card.skill.caster == character and card.skill.is_ultimate) for card in team.current_cards)
             and not team.card_server.check_ultimate(character)):
            team.card_server.try_add_ultimate(Card(character.ultimate, 4))

    def after_move_events(self, team):
        team.tune.after_move()

    def after_merge_events(self, team):
        team.tune.after_merge()

    def turn_start_events(self):
        self.turn += 1
        if self.turn > self.max_turn:
            self.state = State.END
            InfoBroker.battle_end()
            return

        self.input_count = 0
        self.caster_team = self.red_team
        self.target_team = self.blue_team

        while (len(self.red_team.current_cards) < self.red_team.position_count):
            self.red_team.current_cards.extend(self.red_team.card_server.get_next(self.red_team.position_count - len(self.red_team.current_cards)))
            self.evaluate_cards(self.red_team)

        while (len(self.blue_team.current_cards) < self.blue_team.position_count):
            self.blue_team.current_cards.extend(self.blue_team.card_server.get_next(self.blue_team.position_count - len(self.blue_team.current_cards)))
            self.evaluate_cards(self.blue_team)

        for character in self.red_team.members:
            character.update_status_on_turn_start(self.red_team, self.blue_team)

        for character in self.blue_team.members:
            character.update_status_on_turn_start(self.blue_team, self.red_team)
        self.red_team.tune.turn_start()
        self.blue_team.tune.turn_start()
        InfoBroker.turn_start()
    
    def switch_turn_events(self):
        self.caster_team = self.blue_team
        self.target_team = self.red_team
        self.input_count = 0

    def turn_end_events(self):
        for character in self.red_team.members:
            character.update_status_on_turn_end(self.red_team, self.blue_team)

        for character in self.blue_team.members:
            character.update_status_on_turn_end(self.blue_team, self.red_team)

        self.red_team.current_cards = [x for x in self.red_team.current_cards if not x.is_wildcard]
        self.blue_team.current_cards = [x for x in self.blue_team.current_cards if not x.is_wildcard]

        self.evaluate_ultimate_cards()
        InfoBroker.turn_end()

    def after_use_skill_events(self, skill):
        skill.caster.update_status_after_use_skill(skill)
        self.caster_team.tune.after_use_skill()

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
    if len(inputs) != 3:
        return False
    try:
        pos = int(inputs[1])
        target_id = int(inputs[2])
        if pos < 0 or pos >= count:
            return False
        if cards[pos].is_wildcard:
            return False
    except ValueError:
        return False
    return True

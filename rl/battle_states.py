import numpy as np
from gymnasium.spaces import MultiDiscrete
from battle.battlefield import BattleField

def get_observation_space():
    sp = []
    # sp.append(31) # turn_count
    sp.append(4) # input_count
    sp.append(100) # tune_points
    for i in range(8):
        sp.append(100) # skill_id
        sp.append(5) # level
        # sp.append(2) # is_wildcard
    for i in range(3): # red_team
        sp.append(6) # moxie
    #     for j in range(5): # status
    #         sp.append(100) # status_id
    #         sp.append(30) # count
    #         sp.append(100) # value
    for i in range(5): # blue_team_status
        sp.append(100) # status_id
        sp.append(30) # count
        sp.append(100) # value
    return MultiDiscrete(sp)

def battlefield_to_observation(battlefield: BattleField):
    obs = []
    # obs.append(battlefield.turn)
    obs.append(battlefield.input_count)
    obs.append(battlefield.red_team.tune.points)
    
    card_count = 0
    for card in battlefield.red_team.current_cards:
        obs.append(card.skill.id.value)
        obs.append(card.level)
        # obs.append(1 if card.is_wildcard else 0)
        card_count += 1

    while card_count < 8:
        obs.append(0)
        obs.append(0)
        # obs.append(0)
        card_count += 1
    
    for character in battlefield.red_team.members:
        obs.append(character.moxie)
        # status_count = 0
        # for status in character.status:
        #     obs.append(status.id.value)
        #     obs.append(min(status.times_count, status.turn_count, 30))
        #     obs.append(status.value)
        #     status_count += 1
        # while status_count < 5:
        #     obs.append(0)
        #     obs.append(0)
        #     obs.append(0)
        #     status_count += 1
    
    blue_team_status_count = 0
    for status in battlefield.blue_team.members[0].status:
        obs.append(status.id.value)
        obs.append(min(status.times_count, status.turn_count, 30))
        obs.append(status.value)
        blue_team_status_count += 1
    while blue_team_status_count < 5:
        obs.append(0)
        obs.append(0)
        obs.append(0)
        blue_team_status_count += 1
    
    return np.array(obs)

import gymnasium as gym
from gymnasium import spaces
from battle.battlefield import BattleField, State
from characters.bkornblume import Bkornblume
from characters.centurion import Centurion
from characters.enemies import Enemy1
from characters.medicine_pocket import MedicinePocket
from battle.tune import FirstTune
from rl.action_map import action_map
from rl.battle_states import get_observation_space, battlefield_to_observation

def reset_battlefield():
    battle = BattleField(7, 3, [Centurion(), Bkornblume(), MedicinePocket()],FirstTune,
                     4, 1, [Enemy1()], FirstTune)
    return battle

def damage_to_reward(old_dmg, new_dmg):
    dmg = new_dmg - old_dmg
    return dmg

class BattleGym(gym.Env):
    metadata = {"render_modes": ["console"]}

    def __init__(self, grid_size=1, render_mode="console"):
        super(BattleGym, self).__init__()
        self.action_space = spaces.Discrete(len(action_map))
        self.observation_space = get_observation_space()
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)
        self.battlefield = reset_battlefield()
        self.battlefield.start()
        return battlefield_to_observation(self.battlefield), {"dmg": 0}
    
    def step(self, action):
        old_dmg = sum([enemy.max_life - enemy.life for enemy in self.battlefield.blue_team.members])

        self.battlefield.step(action_map[action])
        
        terminated = self.battlefield.state == State.END
        while not terminated and self.battlefield.caster_team == self.battlefield.blue_team:
            self.battlefield.step("u 0 0")
            terminated = self.battlefield.state == State.END

        truncated = False
        new_dmg = 0

        if self.battlefield.bad_input:
            reward = -200
        else:
            new_dmg = sum([enemy.max_life - enemy.life for enemy in self.battlefield.blue_team.members])
            reward = damage_to_reward(old_dmg, new_dmg)
        
        info = {"dmg": new_dmg}

        return (
            battlefield_to_observation(self.battlefield),
            reward - 1600,
            terminated,
            truncated,
            info,
        )

    def render(self, mode="console"):
        if mode != "console":
            return

        print('Turn:' + str(self.battlefield.turn))
        print('Action count: ' + str(self.battlefield.input_count))
        print('Flag: ' + str(self.battlefield.caster_team == self.battlefield.red_team))
        print('Cards:')
        print("\t".join(card.name() for card in self.battlefield.red_team.current_cards))
            
    def close(self):
        pass

# from stable_baselines3.common.env_checker import check_env
# env = BattleGym()
# obs, info = env.reset()
# for i in range(20):
#     env.render()
#     print(obs)
#     obs, r, _, _, dmg = env.step(int(input()))
#     print(r)
    

# check_env(env, warn = True)
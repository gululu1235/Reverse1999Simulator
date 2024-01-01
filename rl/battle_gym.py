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
    battle = BattleField(7, 3, [Centurion(), Bkornblume(), MedicinePocket()], [Enemy1()], FirstTune)
    return battle

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
        return battlefield_to_observation(self.battlefield), {}
    
    def step(self, action):
        old_dmg = sum([enemy.life for enemy in self.battlefield.blue_team])

        self.battlefield.step(action_map[action])
        terminated = self.battlefield.state == State.END
        truncated = False
        if self.battlefield.bad_input:
            reward = -100
        else:
            new_dmg = sum([enemy.life for enemy in self.battlefield.blue_team])
            reward = old_dmg - new_dmg
        
        info = {}

        return (
            battlefield_to_observation(self.battlefield),
            reward,
            terminated,
            truncated,
            info,
        )

    def render(self, mode="console"):
        if mode != "console":
            return

        print('Turn:' + str(self.battlefield.turn))
        print('Action count: ' + str(self.battlefield.action_count))
        print('Tune points: ' + str(self.battlefield.tune.points))
        print('Red team:')
        for character in self.battlefield.red_team:
            status_str = ", ".join(str(status) for status in character.status)
            status =  f"[{status_str}]"
            life_percentage = character.life / character.max_life * 100
            info = [character.name, str(character.life), f"{life_percentage:.2f}%", str(character.moxie), status]
            print("\t".join(info))
        print('Blue team:')
        for character in self.battlefield.blue_team:
            status_str = ", ".join(str(status) for status in character.status)
            status =  f"[{status_str}]"
            life_percentage = character.life / character.max_life * 100
            info = [character.name, str(character.life), f"{life_percentage:.2f}%", str(character.moxie), status]
            print("\t".join(info))
            
    def close(self):
        pass

# from stable_baselines3.common.env_checker import check_env
# env = BattleGym()
# check_env(env, warn = True)
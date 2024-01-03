from matplotlib import pyplot as plt
from stable_baselines3 import PPO
from battle_info.battle_info_broker import InfoBroker
from battle_info.lap_aggregator import LapAggregator
from rl.battle_gym import BattleGym

model = PPO.load("battle_model")
env = BattleGym()
total_episodes = 100
total_rewards = []
damages = []

aggregator = LapAggregator(output_folder='battle_stat')
InfoBroker.register_processor(aggregator)

for episode in range(total_episodes):
    obs, _ = env.reset()
    aggregator.new_lap(env.battlefield)
    episode_reward = 0
    while True:
        action, _states = model.predict(obs)
        obs, reward, done, trunc, info = env.step(int(action))
        episode_reward += reward
        if done or trunc:
            break
    battle = env.battlefield
    total_rewards.append(episode_reward)
    damages.append(sum(c.max_life - c.life for c in battle.blue_team))
    

average_reward = sum(total_rewards) / total_episodes
average_damage = sum(damages) / total_episodes

print("Average Reward:", average_reward)
print("Average Damage:", average_damage)
aggregator.summary()

episodes = list(range(1, len(damages) + 1))
plt.plot(episodes, total_rewards, label='Rewards')
plt.plot(episodes, damages, label='Damages')
plt.xlabel('Episode')
plt.title('Reward & Damage vs. Episodes')
plt.legend()
plt.show()
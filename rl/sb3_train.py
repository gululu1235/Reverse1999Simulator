import os
import gymnasium as gym
import matplotlib.pyplot as plt
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common import results_plotter
from stable_baselines3.common.results_plotter import load_results, ts2xy, plot_results

from rl.battle_gym import BattleGym


def train_model(log_dir):
    # 创建环境
    env = BattleGym()
    env = Monitor(env, log_dir)

    # 创建模型
    model = PPO("MlpPolicy", env, verbose=1)

    # 训练模型
    model.learn(total_timesteps=1000000)

    # 保存模型
    model.save("battle_model")
    env.close()

if __name__ == "__main__":
    log_dir = "sb3_train_monitor/"
    os.makedirs(log_dir, exist_ok=True)
    train_model(log_dir)

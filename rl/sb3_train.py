import os
import gymnasium as gym
import matplotlib.pyplot as plt
from stable_baselines3 import A2C, PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common import results_plotter
from stable_baselines3.common.results_plotter import load_results, ts2xy, plot_results

from rl.battle_gym import BattleGym


def train_model(log_dir):
    policy_kwargs = dict(
        net_arch=[dict(pi=[128, 128], vf=[128, 128])]  # 设置策略 (pi) 和值函数 (vf) 网络的大小
    )
    # 创建环境
    env = BattleGym()
    env = Monitor(env, log_dir, info_keywords=("dmg",))

    # 创建模型
    model = PPO("MlpPolicy", env, policy_kwargs=policy_kwargs, verbose=1, gamma=0)

    # 训练模型
    model.learn(total_timesteps=2000000)

    # 保存模型
    model.save("battle_model")
    env.close()

if __name__ == "__main__":
    log_dir = "sb3_train_monitor/"
    os.makedirs(log_dir, exist_ok=True)
    train_model(log_dir)

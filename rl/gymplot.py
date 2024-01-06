import matplotlib.pyplot as plt

def moving_average(data, window_size):
    return [sum(data[i:i+window_size])/window_size for i in range(len(data)-window_size+1)]

with open("sb3_train_monitor\monitor.csv", 'rt') as fh:
    next(fh)  # 跳过标题行
    next(fh)  # 跳过列标题行
    data = fh.readlines()

# 解析数据
dmgs = [float(line.split(',')[3]) for line in data]
rewards = [float(line.split(',')[0]) for line in data]
episodes = list(range(1, len(rewards) + 1))

# 计算滚动平均奖励
window_size = 50  # 你可以根据需要调整窗口大小
avg_rewards = moving_average(rewards, window_size)
avg_dmgs = moving_average(dmgs, window_size)

print("Last average reward: ", avg_rewards[-1])
print("Last average damage: ", avg_dmgs[-1])

# 绘制奖励图表
plt.plot(episodes, rewards, label='Rewards')
plt.plot(episodes, dmgs, label='Damages')
plt.plot(episodes[:len(avg_rewards)], avg_rewards, label='Average Rewards', color='red')
plt.plot(episodes[:len(avg_dmgs)], avg_dmgs, label='Average Damages', color='green')
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.title('Reward vs. Episodes')
plt.legend()
plt.show()
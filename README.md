# Reverse 1999 Simulator

## Introduction (modified by GPT-4)

Welcome to the simulator for the battle system of [Reverse 1999](https://re1999.bluepoch.com/). Our goal is to create a comprehensive and immersive simulated battle environment, tailored for both interactive human engagement and programmatic applications. This tool is designed to replicate the dynamic and strategic elements of Reverse 1999's battle system, offering users a platform to explore, experiment, and enhance their understanding of the game mechanics.

## Sample usage

### Interactive usage

```bash
.\main.py
```

This will activate a battle where Centurion, Bkornblume and Medicine_pocket against a dummy enermy with reasonable defense stats.

### Supported action

All position indexes below are 0 based.

- m [p1] [p2]: Move card from [p1] to before card [p2].

- u [p1]: Use card on [p1]

- c1: Tune move 1 (refresh card)

- c2: Tune move 2 (Generate wildcard)

- e: End the turn.

- exit: Exit

## Features (modified by GPT-4)

### Easy Extensibility for UX Modification, Battle Data Aggregation and Analysis

The core battle logic of our simulator is built as a state machine, utilizing an event-driven mechanism. This design facilitates easy integration of data analytics, various console outputs, or even distinct user interfaces. To customize, simply implement your own [InfoProcessor](battle_info/info_processor.py) and integrate it as demonstrated in [main.py](main.py). This flexibility allows for seamless modifications and enhancements tailored to your specific needs.

### Gymnasium-Compatible Gym

In pursuit of my personal interest in learning, I have developed a simple model for Reinforcement Learning under the `rl` folder. The observation space currently includes Centurion, Bkornblume, and Medicine_pocket against a single dummy enemy, using basic Proximal Policy Optimization (PPO) for training.

After running a 1-hour training session, the results, as shown in [this figure](sb3_train_monitor/Figure_1.png), appear quite promising. 

#### Training

```bash
python -m rl.sb3_train
```

#### Control Group Performance:

- `USE_0`: Always uses the first card
- `USE_HIGH`: Always selects the card with the highest skill level
- `HUMAN`: My own performance 😎

| Player   | MAX    | MIN    | AVG      |
|----------|--------|--------|----------|
| USE_0    | 141146 | 107977 | 126637.44|
| USE_HIGH | 155434 | 116804 | 137168.68|
| HUMAN    | 164986 | 164986 | 164986.00|
| PPO*     | 170030 | 101699 | 132044.86|

*Note: For PPO, this data represents the last 50 rewards. The rewards calculation is based on damage minus penalty for incorrect inputs. The actual damage figures are higher than those shown in the table.


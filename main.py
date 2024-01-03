from stable_baselines3 import PPO
from battle_info.battle_info_broker import InfoBroker
from battle_info.battle_stat_aggregator import BattleStatAggregator
from battle_info.console_logger import ConsoleLogger
from battle.battlefield import BattleField, State
from characters.bkornblume import Bkornblume
from characters.centurion import Centurion
from characters.enemies import Enemy1
from characters.medicine_pocket import MedicinePocket
from battle.tune import FirstTune
from rl.action_map import action_map
from rl.battle_states import battlefield_to_observation

model = PPO.load("battle_model")

battle = BattleField(7, 3, [Centurion(), Bkornblume(), MedicinePocket()], [Enemy1()], FirstTune)
InfoBroker.register_processor(ConsoleLogger(battle))
InfoBroker.register_processor(BattleStatAggregator(battle, output_folder='battle_stat'))
battle.start()


def print_cards():
    print('Cards:')
    print("\t".join(card.name() for card in battle.current_cards))

while battle.state == State.RUNNING:
    print_cards()
    action, _states = model.predict(battlefield_to_observation(battle))
    hint = action_map[int(action)]
    user_input = input(f"Action {str(battle.input_count + 1)}/{str(battle.action_count)} (hint: {hint}):")
    #user_input = "u 0"
    battle.step(user_input)

dmg_done = sum(c.max_life - c.life for c in battle.blue_team)
print(f"Battle ends in turn {battle.turn}. Total damage done: {dmg_done}")
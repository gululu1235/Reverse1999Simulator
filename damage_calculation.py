from dmg_type import DamageType
from characters.centurion import *
from characters.enemies import *

def calc_damage(attacker, attackee, damage_type, skill_ratio, is_ultimate, is_critical, is_matchup):
    defense = 0
    if damage_type == DamageType.PHYSICAL:
        defense = attackee.properties.reallity_def
    elif damage_type == DamageType.MENTAL:
        defense = attackee.properties.mental_def

    might_multiplier = 1 + (attacker.properties.ultimate_might if is_ultimate else attacker.properties.incantation_might)
    matchup_multiplier = 1.3 if is_matchup else 1
    crit_multiplier = attacker.properties.critical_dmg - attackee.properties.critical_def if is_critical else 1
    return ((attacker.attack - defense)
             * (1 + attacker.properties.dmg_bonus - attackee.properties.dmg_taken_reduction)
             * skill_ratio * might_multiplier * matchup_multiplier * crit_multiplier)

# attacker = Centurion()
# enemy = Enemy1()

# for _ in range(4):
#     attacker.reset_current_properties()
#     attacker.moxie += 1
#     for status in attacker.status:
#         status.PropertyImpact()
    
#     print(calc_damage(attacker, enemy, DamageType.PHYSICAL, 1.5, False, True, False))

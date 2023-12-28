from dmg_type import DamageType

def calc_damage(attacker, attackee, damage_type, skill_ratio, is_ultimate, is_critical, is_matchup):
    attack = attacker.attack * (1 + attacker.properties.attack_bonus_rate)
    defense = 0
    if damage_type == DamageType.PHYSICAL:
        defense = attackee.properties.reality_def * (1 + attackee.properties.reality_def_bonus_rate)
    elif damage_type == DamageType.MENTAL:
        defense = attackee.properties.mental_def * (1 + attackee.properties.mental_def_bonus_rate)
    defense = defense * (1 - attacker.properties.penetration_rate)

    attack_multiplier = max(attack * 0.1, attack - defense)

    might_multiplier = max(0, 1 + (attacker.properties.ultimate_might if is_ultimate else attacker.properties.incantation_might))
    dmg_multiplier = max(0.3, 1 + attacker.properties.dmg_bonus - attackee.properties.dmg_taken_reduction)
    matchup_multiplier = 1.3 if is_matchup else 1
    crit_multiplier = min(1.1, attacker.properties.critical_dmg - attackee.properties.critical_def) if is_critical else 1

    return int(int(attack_multiplier * skill_ratio)
             * dmg_multiplier
             * might_multiplier * matchup_multiplier * crit_multiplier)

def calc_heal(caster, target, skill_ratio, is_critical):
    attack = caster.attack * (1 + caster.properties.attack_bonus_rate)
    crit_multiplier = (caster.properties.critical_dmg - 1) * 0.3 + 1 if is_critical else 1
    return int(int(attack * skill_ratio)
               * crit_multiplier
               * (1 + caster.properties.healing_done_bonus)
               * (1 + target.properties.healing_taken_bonus))
# Reverse 1999 Simulator

## Sample usage

### Run the simulator

```bash
.\battlefield.py
```

### Supported action

All position indexes below are 0 based.

- m [p1] [p2]: Move card from [p1] to before card [p2]. The index number is 0 based.

- u [p1]: Use card on [p1]

- c1: Chord move 1 (refresh card)

- c2: Chord move 2 (Generate wildcard)

- e: End the turn.

### Sample output

```text
Reset cards
Turn:1
Chord points: 20
Red team:
Centurion_330101        9152    100.00% 0       []
Bkornblume_320105       8797    100.00% 0       []
MedicinePocket_301090   9853    100.00% 0       []
Blue team:
Enemy1  999999  100.00% 0       []
Cards:
VictoriousGeneral_1     AlchemyWare_1   PryingEar_1     InherentHabit_1 OutdoorSuperstar_1      WatchHerSleeves_1       VictoriousGeneral_1
Action 1:m 6 0
Cards:
VictoriousGeneral_2     AlchemyWare_1   PryingEar_1     InherentHabit_1 OutdoorSuperstar_1      WatchHerSleeves_1
Action 2:u 0
Cards:
AlchemyWare_1   PryingEar_1     InherentHabit_1 OutdoorSuperstar_1      WatchHerSleeves_1
Action 3:u 3
Cards:
AlchemyWare_1   PryingEar_1     InherentHabit_1 WatchHerSleeves_1
Executing card: Move
Executing card: VictoriousGeneral_2
attacker: Centurion_330101 target: Enemy1 dmg: 5649 life: 994350 critical: True
Executing card: OutdoorSuperstar_1
attacker: Centurion_330101 target: Enemy1 dmg: 2436 life: 991914 critical: False
**************************************
Turn:2
Chord points: 38
Red team:
Centurion_330101        9152    100.00% 4       []
Bkornblume_320105       8797    100.00% 0       []
MedicinePocket_301090   9853    100.00% 0       []
Blue team:
Enemy1  991914  99.19%  0       []
Cards:
AlchemyWare_1   PryingEar_1     InherentHabit_1 WatchHerSleeves_1       AlchemyWare_1   VictoriousGeneral_1     PryingEar_1
Action 1:
```

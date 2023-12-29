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

- exit: Exit

### Sample console output

```text
PS E:\projects\Reverse1999Simulator> & c:/Windows/py.exe e:/projects/Reverse1999Simulator/battlefield.py
Reset cards
Turn:1 starts.
Chord points: 20
Red team:
Centurion_330101        9152    100.00% 0       []
Bkornblume_320105       8797    100.00% 0       []
MedicinePocket_301090   9853    100.00% 0       []
Blue team:
Enemy1  999999  100.00% 0       []
Cards:
AlchemyWare_1   WatchHerSleeves_1       VictoriousGeneral_1     OutdoorSuperstar_1      InherentHabit_1 PryingEar_1     AlchemyWare_1
Action 1:m 6 0
Cards:
AlchemyWare_2   WatchHerSleeves_1       VictoriousGeneral_1     OutdoorSuperstar_1      InherentHabit_1 PryingEar_1
Action 2:u 0
Cards:
WatchHerSleeves_1       VictoriousGeneral_1     OutdoorSuperstar_1      InherentHabit_1 PryingEar_1
Action 3:u 0
Cards:
VictoriousGeneral_1     OutdoorSuperstar_1      InherentHabit_1 PryingEar_1
Executing card: Move
Executing card: AlchemyWare_2
healer: MedicinePocket_301090 target: MedicinePocket_301090 heal: 0 life: 9853 critical: False
healer: MedicinePocket_301090 target: Bkornblume_320105 heal: 0 life: 8797 critical: False
healer: MedicinePocket_301090 target: Centurion_330101 heal: 0 life: 9152 critical: False
Executing card: WatchHerSleeves_1
attacker: Bkornblume_320105 target: Enemy1 dmg: 1543 life: 998456 critical: False
Turn1 ends.
*******************************************************
Turn:2 starts.
Chord points: 38
Red team:
Centurion_330101        9152    100.00% 0       [Sturdiness_1t]
Bkornblume_320105       8797    100.00% 1       [Sturdiness_1t]
MedicinePocket_301090   9853    100.00% 3       [Sturdiness_1t]
Blue team:
Enemy1  998456  99.85%  0       []
Cards:
VictoriousGeneral_1     OutdoorSuperstar_1      InherentHabit_1 PryingEar_1     OutdoorSuperstar_1      AlchemyWare_1   VictoriousGeneral_1
Action 1:u 0
Cards:
OutdoorSuperstar_1      InherentHabit_1 PryingEar_1     OutdoorSuperstar_1      AlchemyWare_1   VictoriousGeneral_1
Action 2:u 0
Cards:
InherentHabit_1 PryingEar_1     OutdoorSuperstar_1      AlchemyWare_1   VictoriousGeneral_1
Action 3:u 0
Cards:
PryingEar_1     OutdoorSuperstar_1      AlchemyWare_1   VictoriousGeneral_1
Executing card: VictoriousGeneral_1
attacker: Centurion_330101 target: Enemy1 dmg: 2670 life: 995786 critical: False
Executing card: OutdoorSuperstar_1
attacker: Centurion_330101 target: Enemy1 dmg: 2188 life: 993598 critical: False
Executing card: InherentHabit_1
attacker: MedicinePocket_301090 target: Enemy1 dmg: 1412 life: 992186 critical: False
Turn2 ends.
*******************************************************
Turn:3 starts.
Chord points: 55
Red team:
Centurion_330101        9152    100.00% 2       [Sturdiness_1t]
Bkornblume_320105       8797    100.00% 1       [Sturdiness_1t]
MedicinePocket_301090   9853    100.00% 4       [Sturdiness_1t]
Blue team:
Enemy1  992186  99.22%  0       []
Cards:
PryingEar_1     OutdoorSuperstar_1      AlchemyWare_1   VictoriousGeneral_1     InherentHabit_1 OutdoorSuperstar_1      PryingEar_1
Action 1:exit
Turn3 ends.
*******************************************************
```

### Sample battle stats

Currently the tool outputs a csv file for a turn-based battle stat.

```csv
turn,color,character,move_count,damage,heal
1,red,Centurion_330101,0,0,0
1,red,Bkornblume_320105,1,1543,0
1,red,MedicinePocket_301090,2,0,0
1,blue,Enemy1,0,0,0
2,red,Centurion_330101,2,4858,0
2,red,Bkornblume_320105,1,1543,0
2,red,MedicinePocket_301090,3,1412,0
2,blue,Enemy1,0,0,0
3,red,Centurion_330101,2,4858,0
3,red,Bkornblume_320105,1,1543,0
3,red,MedicinePocket_301090,3,1412,0
3,blue,Enemy1,0,0,0

```

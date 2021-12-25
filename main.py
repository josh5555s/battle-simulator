from armies import armies

# full attack turn
def attackTurn():
  # everyone attacks
  for army in armies:
    # print(f'------- \n {army.color} army attacks! \n-------')
    for attacker in army.units:
      # input() # to observe turn by turn
      # print(attacker.__dict__)
      target = attacker.select_attack_target()

      attack = attacker.attack()
      if attack['hits']: 
        attack_outcome_text = attack['outcome_text'] 
      else:
        attack_outcome_text = 'misses.'

      print(f'{attacker.full_name}({attacker.health}) {attacker.attack_verb} at {target.full_name}({target.health}) and {attack_outcome_text}')

      if attack['hits']: 
        target.health -= attack['damage']
        if target.health < 1:
          target.alive = False

  # post attack status
  for army in armies:
    # print(f'------- \n {army.color} army post-attack status \n-------')
    for unit in army.units:
      # print(unit.name, 'The', unit.color, '-', unit.health, unit.alive, 'current attacker: ', unit.currentAttacker)
      if unit.health < 1:
        army.units.remove(unit)
  check_next_turn()

# check if there should be another turn
def check_next_turn():
  surviving_army = []
  for army in armies:
    # print(f'-------- \n{army.color}Army has {len(army.units)} units left')
    if len(army.units) > 0:
      surviving_army.append(army)
  if len(surviving_army) > 1: 
    attackTurn()
  elif len(surviving_army) == 1:
    print(surviving_army[0].name, 'wins!')
  else:
    print("Everyone is dead, so let's call it a draw...")

check_next_turn()

from abc import ABC, abstractmethod
import random
from names import names


class Army:
    def __init__(self, color, swordsmen_count, archer_count):
        self.name = f'The {color} Army'
        self.color = color
        self.units = []
        self.defeated = False
        self.kills = 0
        for s in range(swordsmen_count):
            self.units.append(Swordsman(color))
        for a in range(archer_count):
            self.units.append(Archer(color))


class Unit(ABC):
    def __init__(self, color):
        name = random.choice(names)
        names.remove(name)
        self.name = name
        self.color = color
        self.__health = 100
        self.__alive = True
        self.currentAttacker = 'none'
        self.kills = 0

    @abstractmethod
    def select_attack_target(self):
        pass

    def attack(self):
        attack = {
            "hits": False,
            "hit_type": 'misses',
            "damage": 0,
        }
        attempt = random.random()
        damage = random.randrange(self.min_damage, self.max_damage)
        if self.min_hit_chance > attempt < self.crit_hit_chance:
            attack['hits'] = True
            attack['damage'] = damage
            attack['outcome_text'] = f'gets a body hit for {damage} damage.'
        elif attempt > self.crit_hit_chance:
            damage *= self.crit_multiplyer
            attack['hits'] = True
            attack['damage'] = damage
            attack['outcome_text'] = f'gets a headshot for {damage} damage.'
        return attack

    def get_health(self):
        return self.__health

    def take_damage(self, damage):
        if damage < self.__health:
            self.__health -= damage
        else:
            self.__health = 0
            self.__alive = False

    def is_alive(self):
        return self.__alive


class Swordsman(Unit):
    def __init__(self, color):
        super().__init__(color)
        self.type = 'Swordsman'
        self.full_name = f'{self.name} The {self.color} {self.type}'
        self.attack_verb = 'swings'
        self.armour = 40
        self.min_hit_chance = .2
        self.crit_hit_chance = .8
        self.min_damage = 30
        self.max_damage = 60
        self.crit_multiplyer = 2

    def select_attack_target(self):
        def find_other_army(armies):
            selected_army = random.choice(armies)
            if selected_army.color != self.color and len(selected_army.units) > 0:
                unit_is_swordsman = []
                unit_not_swordsman = []
                # if there are still swordsmen then must attack swordsmen
                for unit in selected_army.units:
                    if isinstance(unit, Swordsman):
                        unit_is_swordsman.append(unit)
                    else:
                        unit_not_swordsman.append(unit)
                if len(unit_is_swordsman):
                    selected_unit = random.choice(unit_is_swordsman)
                else:
                    selected_unit = random.choice(unit_not_swordsman)
                return selected_unit
            else:
                selected_unit = find_other_army(armies)
                return selected_unit
        selected_unit = find_other_army(armies)
        return selected_unit


class Archer(Unit):
    def __init__(self, color):
        super().__init__(color)
        self.type = 'Archer'
        self.full_name = f'{self.name} The {self.color} {self.type}'
        self.attack_verb = 'fires'
        self.armour = 10
        self.arrow_count = 10
        self.min_hit_chance = .4
        self.crit_hit_chance = .9
        self.min_damage = 50
        self.max_damage = 100
        self.crit_multiplyer = 3

    def select_attack_target(self):
        def find_other_army(armies):
            selected_army = random.choice(armies)
            if selected_army.color != self.color and len(selected_army.units) > 0:
                selected_unit = random.choice(selected_army.units)
                return selected_unit
            else:
                selected_unit = find_other_army(armies)
                return selected_unit
        selected_unit = find_other_army(armies)
        return selected_unit


armies = [
    Army('Red', swordsmen_count=2, archer_count=1),
    Army('Blue', swordsmen_count=2, archer_count=1),
    # Army('Green', swordsmen_count=2, archer_count=1),
]

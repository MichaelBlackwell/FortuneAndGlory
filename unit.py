class Unit:
    def __init__(self, name, sprite, unit_type, fire_strength, attack_type, morale, defense_strength, defense_type, movement, movement_type, fire_range):
        self.name = name
        self.unit_type = unit_type
        self.fire_strength = fire_strength
        self.attack_type = attack_type
        self.morale = morale
        self.defense_strength = defense_strength
        self.defense_type = defense_type
        self.movement = movement
        self.movement_type = movement_type
        self.fire_range = fire_range
        self.steps = 1
        self.x = 0
        self.y = 0
        self.mode = "Fire"
        self.dug_in = False
        self.morale_mode = "Fine" # suppressed, retreat, paralyzed

    def draw
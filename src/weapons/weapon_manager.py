from ursina import *
from src.weapons.weapon_base import WeaponBase

class WeaponManager:
    def __init__(self, player):
        self.player = player
        self.weapons = {}
        self.current_weapon = None
        self.setup_weapons()

    def setup_weapons(self):
        # Initialize all weapons
        weapon_types = ['pistol', 'rifle']
        
        for weapon_type in weapon_types:
            self.weapons[weapon_type] = WeaponBase(weapon_type, self.player)
            self.weapons[weapon_type].disable()
            
        # Set default weapon
        self.switch_weapon('pistol')

    def switch_weapon(self, weapon_type):
        if weapon_type not in self.weapons:
            return
            
        # Disable current weapon
        if self.current_weapon:
            self.current_weapon.disable()
            
        # Enable new weapon
        self.current_weapon = self.weapons[weapon_type]
        self.current_weapon.enable()

    def update(self):
        if self.current_weapon:
            # Handle weapon input
            if mouse.left:
                self.current_weapon.shoot()
                
            if held_keys['r']:
                self.current_weapon.reload()
                
            # Weapon switching
            if held_keys['1']:
                self.switch_weapon('pistol')
            elif held_keys['2']:
                self.switch_weapon('rifle')

    def disable_all_weapons(self):
        for weapon in self.weapons.values():
            weapon.disable()

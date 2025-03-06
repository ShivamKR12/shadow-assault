from ursina import *

class WeaponHUD(Entity):
    def __init__(self, weapon_manager):
        super().__init__(
            parent=camera.ui
        )
        
        self.weapon_manager = weapon_manager
        
        # Ammo counter
        self.ammo_text = Text(
            parent=self,
            text='',
            position=(-0.85, -0.45),
            scale=2
        )
        
        # Weapon name
        self.weapon_name = Text(
            parent=self,
            text='',
            position=(-0.85, -0.4),
            scale=1.5
        )

    def update(self):
        if self.weapon_manager.current_weapon:
            weapon = self.weapon_manager.current_weapon
            self.ammo_text.text = f'{weapon.ammo}/{weapon.max_ammo}'
            self.weapon_name.text = weapon.weapon_type.capitalize()
            
            # Change color if reloading
            self.ammo_text.color = color.gray if weapon.is_reloading else color.white

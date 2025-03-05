from ursina import *

class WeaponPickup(Entity):
    def __init__(self, weapon_type, position):
        super().__init__(
            position=position,
            model=WEAPON_TYPES[weapon_type]['model_path'],
            scale=0.5,
            rotation_y=random.uniform(0, 360)
        )
        
        self.weapon_type = weapon_type
        
        # Add floating animation
        self.y_offset = 0
        self.animate_y_offset = 0.5
        self.rotation_

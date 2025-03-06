from ursina import *
from src.config.weapon_config import WEAPON_DATA
import random
import math

class WeaponBase(Entity):
    def __init__(self, weapon_type, player):
        super().__init__(
            parent=camera,
            position=WEAPON_DATA[weapon_type]['position'],
            scale=WEAPON_DATA[weapon_type]['scale']
        )
        
        self.weapon_type = weapon_type
        self.player = player
        self.config = WEAPON_DATA[weapon_type]
        
        # Load weapon model and texture
        self.model = self.config['model_path']
        self.texture = self.config['texture_path']
        
        # Weapon state
        self.ammo = self.config['magazine_size']
        self.max_ammo = self.config['magazine_size']
        self.is_reloading = False
        self.last_shot_time = 0
        
        # Recoil state
        self.recoil_offset = Vec3(0, 0, 0)
        self.recoil_recovery_velocity = Vec3(0, 0, 0)
        self.original_position = self.position
        
        # Sound effects
        self.sounds = {
            'shoot': Audio(self.config['sound_effects']['shoot'], loop=False, autoplay=False),
            'reload': Audio(self.config['sound_effects']['reload'], loop=False, autoplay=False),
            'empty': Audio(self.config['sound_effects']['empty'], loop=False, autoplay=False)
        }

    def shoot(self):
        current_time = time.time()
        if current_time - self.last_shot_time < self.config['fire_rate']:
            return False
            
        if self.is_reloading:
            return False
            
        if self.ammo <= 0:
            self.sounds['empty'].play()
            return False
            
        # Perform raycast for hit detection
        hit_info = raycast(
            camera.world_position,
            camera.forward,
            distance=100,
            ignore=[self, self.player]
        )
        
        if hit_info.hit:
            # Handle hit effects here
            if hasattr(hit_info.entity, 'take_damage'):
                hit_info.entity.take_damage(self.config['damage'])
                
        # Apply recoil
        self.apply_recoil()
        
        # Play shooting effects
        self.sounds['shoot'].play()
        self.muzzle_flash()
        
        # Update weapon state
        self.ammo -= 1
        self.last_shot_time = current_time
        return True

    def reload(self):
        if self.is_reloading or self.ammo == self.max_ammo:
            return
            
        self.is_reloading = True
        self.sounds['reload'].play()
        
        # Start reload animation
        self.animate_reload()
        
        # Schedule reload completion
        invoke(self.complete_reload, delay=self.config['reload_time'])

    def complete_reload(self):
        self.ammo = self.max_ammo
        self.is_reloading = False

    def apply_recoil(self):
        # Vertical recoil
        vertical = random.uniform(
            self.config['recoil']['vertical'][0],
            self.config['recoil']['vertical'][1]
        )
        
        # Horizontal recoil
        horizontal = random.uniform(
            self.config['recoil']['horizontal'][0],
            self.config['recoil']['horizontal'][1]
        )
        
        # Apply recoil to weapon position
        self.recoil_offset.y += vertical
        self.recoil_offset.x += horizontal
        
        # Apply recoil to camera
        camera.rotation_x -= vertical
        camera.rotation_y += horizontal

    def update(self):
        # Handle recoil recovery
        recovery_speed = self.config['recoil']['recovery_speed'] * time.dt
        
        # Recover weapon position
        self.recoil_offset = self.recoil_offset.lerp(
            Vec3(0, 0, 0),
            recovery_speed
        )
        self.position = self.original_position + self.recoil_offset

    def muzzle_flash(self):
        # Create muzzle flash effect
        flash = Entity(
            parent=self,
            model='quad',
            scale=0.2,
            color=color.yellow,
            position=Vec3(0, 0.1, -1),
            billboard=True
        )
        
        # Destroy flash after short duration
        destroy(flash, delay=0.05)

    def animate_reload(self):
        # Simple reload animation
        original_pos = self.position
        down_pos = self.position + Vec3(0, -0.2, 0)
        
        # Animate down
        self.animate_position(
            down_pos,
            duration=self.config['reload_time'] * 0.3
        )
        
        # Animate up
        self.animate_position(
            original_pos,
            duration=self.config['reload_time'] * 0.3,
            delay=self.config['reload_time'] * 0.7
        )

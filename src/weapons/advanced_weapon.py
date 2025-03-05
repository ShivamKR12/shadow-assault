from ursina import *
from src.config.weapon_config import WEAPON_TYPES, MODIFICATION_TYPES
import math

class AdvancedWeapon(Entity):
    def __init__(self, weapon_type, player):
        super().__init__(
            parent=camera.ui,
            model=WEAPON_TYPES[weapon_type]['model_path'],
            scale=0.1
        )
        
        self.weapon_type = weapon_type
        self.config = WEAPON_TYPES[weapon_type]
        self.player = player
        
        # Weapon state
        self.ammo = self.config['magazine_size']
        self.max_ammo = self.config['magazine_size']
        self.is_reloading = False
        self.is_ads = False
        self.last_shot_time = 0
        
        # Modifications
        self.modifications = {
            'scope': None,
            'barrel': None,
            'magazine': None
        }
        
        # Animation system
        self.animator = WeaponAnimator(self)
        
        # Weapon sway
        self.original_position = self.position
        self.target_position = self.position
        self.sway_amount = self.config['sway_amount']
        self.sway_speed = 5
        self.bob_amount = 0.02
        self.bob_speed = 5
        self.walk_cycle = 0
        
        # ADS
        self.ads_position = self.config['ads_position']
        self.ads_fov = self.config['ads_fov']
        self.original_fov = camera.fov
        self.ads_speed = 8
        self.ads_lerp = 0

    def update(self):
        if not self.is_reloading:
            # Handle shooting
            if self.can_shoot():
                if self.config['type'] == 'auto' and mouse.left:
                    self.shoot()
                elif self.config['type'] in ['semi', 'pump'] and mouse.left.pressed:
                    self.shoot()
            
            # Handle reloading
            if held_keys['r'] and self.ammo < self.max_ammo:
                self.start_reload()
        
        # Update weapon position and sway
        self.update_weapon_position()
        
        # Update ADS
        self.update_ads()

    def update_weapon_position(self):
        # Calculate weapon sway based on mouse movement
        mouse_delta = Vec2(
            mouse.velocity[0],
            mouse.velocity[1]
        )
        
        sway_offset = Vec3(
            -mouse_delta.x * self.sway_amount.x,
            -mouse_delta.y * self.sway_amount.y,
            0
        )
        
        # Add walk cycle bob
        if self.player.velocity.length() > 0.1:
            self.walk_cycle += time.dt * self.bob_speed
            bob_offset = Vec3(
                math.sin(self.walk_cycle) * self.bob_amount,
                math.cos(self.walk_cycle * 2) * self.bob_amount,
                0
            )
        else:
            bob_offset = Vec3(0, 0, 0)
            self.walk_cycle = 0
        
        # Calculate target position
        target_pos = (
            self.original_position +
            sway_offset +
            bob_offset
        )
        
        # Lerp to target position
        self.position = lerp(
            self.position,
            target_pos,
            time.dt * self.sway_speed
        )

    def update_ads(self):
        # Update ADS state
        if mouse.right:
            self.ads_lerp = min(1, self.ads_lerp + time.dt * self.ads_speed)
        else:
            self.ads_lerp = max(0, self.ads_lerp - time.dt * self.ads_speed)
        
        # Apply ADS position and FOV
        self.position = lerp(
            self.original_position,
            self.ads_position,
            self.ads_lerp
        )
        
        camera.fov = lerp(
            self.original_fov,
            self.ads_fov,
            self.ads_lerp
        )

    def shoot(self):
        if self.ammo <= 0 or time.time() - self.last_shot_time < self.config['fire_rate']:
            return
        
        # Handle different weapon types
        if self.config['type'] == 'shotgun':
            self.shoot_shotgun()
        else:
            self.shoot_single()
        
        # Update state
        self.ammo -= 1
        self.last_shot_time = time.time()
        
        # Play animations and effects
        self.animator.play('fire')
        self.create_muzzle_flash()
        self.apply_recoil()

    def shoot_single(self):
        # Calculate accuracy
        spread = (1 - self.config['accuracy']) * (0.5 if self.is_ads else 1.0)
        
        direction = camera.forward + Vec3(
            random.uniform(-spread, spread),
            random.uniform(-spread, spread),
            random.uniform(-spread, spread)
        ).normalized()
        
        # Raycast
        hit_info = raycast(
            camera.world_position,
            direction,
            distance=self.config['range'],
            ignore=[self, self.player]
        )
        
        if hit_info.hit:
            self.create_impact_effect(hit_info.point, hit_info.normal)
            if hasattr(hit_info.entity, 'take_damage'):
                hit_info.entity.take_damage(self.config['damage'])

    def shoot_shotgun(self):
        for _ in range(self.config['pellets']):
            spread = (1 - self.config['accuracy']) * (0.5 if self.is_ads else 1.0)
            direction = camera.forward + Vec3(
                random.uniform(-spread, spread),
                random.uniform(-spread, spread),
                random.uniform(-spread, spread)
            ).normalized()
            
            hit_info = raycast(
                camera.world_position,
                direction,
                distance=self.config['range'],
                ignore=[self, self.player]
            )
            
            if hit_info.hit:
                self.create_impact_effect(hit_info.point, hit_info.normal)
                if hasattr(hit_info.entity, 'take_damage'):
                    hit_info.entity.take_damage(self.config['damage'])

    def start_reload(self):
        self.is_reloading = True
        reload_time = self.config['reload_time']
        
        # Apply magazine modification if present
        if self.modifications['magazine']:
            reload_time *= self.modifications['magazine']['reload_time_multiplier']
        
        if self.config['type'] == 'shotgun':
            self.reload_shotgun()
        else:
            self.animator.play('reload')
            invoke(self.complete_reload, delay=reload_time)

    def reload_shotgun(self):
        self.animator.play('reload_start')
        
        # Calculate shells needed
        shells_to_reload = self.max_ammo - self.ammo
        total_reload_time = self.config['reload_time'] * shells_to_reload
        
        # Play insert animation for each shell
        for i in range(shells_to_reload):
            invoke(
                self.animator.play,
                args=['reload_insert'],
                delay=self.config['reload_time'] * (i + 1)
            )
        
        # Complete reload
        invoke(
            Sequence(
                Func(self.animator.play, 'reload_end'),
                Func(self.complete_reload)
            ),
            delay=total_reload_time
        )

    def complete_reload(self):
        self.ammo = self.max_ammo
        self.is_reloading = False

    def add_modification(self, slot, mod_type):
        if slot in self.modifications and mod_type in MODIFICATION_TYPES[slot]:
            mod = MODIFICATION_TYPES[slot][mod_type]
            self.modifications[slot] = mod
            
            # Apply modification effects
            if slot == 'scope':
                self.ads_fov = self.config['ads_fov'] + mod['ads_fov']
            elif slot == 'magazine':
                self.max_ammo = int(self.config['magazine_size'] * mod['capacity_multiplier'])

    def remove_modification(self, slot):
        if slot in self.modifications:
            self.modifications[slot] = None
            
            # Reset modification effects
            if slot == 'scope':
                self.ads_fov = self.config['ads_fov']
            elif slot == 'magazine':
                self.max_ammo = self.config['magazine_size']

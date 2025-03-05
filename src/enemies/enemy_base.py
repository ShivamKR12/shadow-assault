from ursina import *
from src.config.enemy_config import ENEMY_TYPES
import random
import math

class EnemyBase(Entity):
    def __init__(self, enemy_type, player, nav_mesh):
        super().__init__()
        self.enemy_type = enemy_type
        self.config = ENEMY_TYPES[enemy_type]
        self.player = player
        self.nav_mesh = nav_mesh
        
        # Set up enemy model and properties
        self.model = self.config['model_path']
        self.texture = self.config['texture_path']
        self.scale = self.config['scale']
        self.color = self.config['color']
        self.collider = 'box'
        
        # Enemy stats
        self.health = self.config['health']
        self.speed = self.config['speed']
        self.damage = self.config['damage']
        
        # AI state
        self.state = 'idle'
        self.path = []
        self.current_path_index = 0
        self.last_attack_time = 0
        self.target_position = None
        
        # Health bar
        self.health_bar = Entity(
            parent=self,
            model='quad',
            color=color.green,
            scale=(1.5, 0.1),
            billboard=True,
            y=2
        )

    def update(self):
        if self.health <= 0:
            return
            
        self.update_state()
        self.update_behavior()
        self.update_health_bar()

    def update_state(self):
        distance_to_player = (self.player.position - self.position).length()
        
        if distance_to_player <= self.config['attack_range']:
            self.state = 'attack'
        elif distance_to_player <= self.config['detection_range']:
            self.state = 'chase'
        else:
            self.state = 'idle'

    def update_behavior(self):
        if self.state == 'attack':
            self.perform_attack()
        elif self.state == 'chase':
            self.chase_player()
        elif self.state == 'idle':
            self.idle_behavior()

    def chase_player(self):
        # Update path every few seconds or when player moves significantly
        if not self.path or (time.time() - self.last_path_update > 1.0):
            self.update_path_to_player()
            
        if self.path and self.current_path_index < len(self.path):
            target = self.path[self.current_path_index]
            direction = (target - self.position).normalized()
            
            # Move towards next waypoint
            self.position += direction * self.speed * time.dt
            
            # Look at movement direction
            self.look_at_2d(self.position + direction)
            
            # Check if reached waypoint
            if (target - self.position).length() < 0.5:
                self.current_path_index += 1

    def update_path_to_player(self):
        self.path = self.nav_mesh.find_path(self.position, self.player.position)
        self.current_path_index = 0
        self.last_path_update = time.time()

    def perform_attack(self):
        current_time = time.time()
        if current_time - self.last_attack_time >= self.config['attack_cooldown']:
            # Face player
            self.look_at_2d(self.player.position)
            
            # Deal damage
            distance = (self.player.position - self.position).length()
            if distance <= self.config['attack_range']:
                self.player.take_damage(self.damage)
                self.last_attack_time = current_time

    def idle_behavior(self):
        # Simple patrol or idle animation could be implemented here
        pass

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        # Spawn particles
        self.spawn_death_particles()
        
        # Add score
        if hasattr(self.player, 'add_score'):
            self.player.add_score(self.config['points'])
            
        # Disable enemy
        self.disable()
        destroy(self, delay=1)

    def spawn_death_particles(self):
        for _ in range(20):
            particle = Entity(
                model='sphere',
                color=self.color,
                position=self.position + Vec3(
                    random.uniform(-0.5, 0.5),
                    random.uniform(0, 1),
                    random.uniform(-0.5, 0.5)
                ),
                scale=0.2
            )
            
            # Add random velocity
            particle.animate_position(
                particle.position + Vec3(
                    random.uniform(-2, 2),
                    random.uniform(1, 3),
                    random.uniform(-2, 2)
                ),
                duration=0.5,
                curve=curve.out_expo
            )
            
            # Fade out and destroy
            particle.animate_scale(0, duration=0.5, curve=curve.linear)
            destroy(particle, delay=0.5)

    def update_health_bar(self):
        health_percentage = self.health / self.config['health']
        self.health_bar.scale_x = 1.5 * health_percentage
        self.health_bar.color = color.lerp(color.red, color.green, health_percentage)

    def look_at_2d(self, target_pos):
        # Only rotate on Y axis (2D rotation)
        direction = target_pos - self.position
        self.rotation_y = math.degrees(math.atan2(-direction.x, -direction.z))

from ursina import *
import random
import math

class EnemyAI:
    def __init__(self, enemy):
        self.enemy = enemy
        self.state = 'idle'
        self.target = None
        self.path = []
        self.next_waypoint = None
        self.last_attack_time = 0
        self.last_path_update = 0
        self.path_update_interval = 1.0
        
    def update(self, dt):
        if self.enemy.health <= 0:
            return
            
        # Update state based on behavior type
        if self.enemy.config['behavior'] == 'chase':
            self.update_chase_behavior(dt)
        elif self.enemy.config['behavior'] == 'ranged':
            self.update_ranged_behavior(dt)
        elif self.enemy.config['behavior'] == 'tank':
            self.update_tank_behavior(dt)
        elif self.enemy.config['behavior'] == 'boss':
            self.update_boss_behavior(dt)

    def update_chase_behavior(self, dt):
        distance_to_player = (self.enemy.player.position - self.enemy.position).length()
        
        if distance_to_player <= self.enemy.config['attack_range']:
            self.state = 'attack'
            self.perform_attack()
        elif distance_to_player <= self.enemy.config['detection_range']:
            self.state = 'chase'
            self.update_path_to_player()
            self.follow_path(dt)
        else:
            self.state = 'idle'
            self.patrol(dt)

    def update_ranged_behavior(self, dt):
        distance_to_player = (self.enemy.player.position - self.enemy.position).length()
        
        if distance_to_player <= self.enemy.config['attack_range']:
            # Move away if too close
            if distance_to_player < self.enemy.config['attack_range'] * 0.5:
                self.state = 'retreat'
                self.retreat_from_player(dt)
            else:
                self.state = 'attack'
                self.perform_ranged_attack()
        elif distance_to_player <= self.enemy.config['detection_range']:
            self.state = 'position'
            self.find_shooting_position(dt)
        else:
            self.state = 'idle'
            self.patrol(dt)

    def update_tank_behavior(self, dt):
        distance_to_player = (self.enemy.player.position - self.enemy.position).length()
        
        if distance_to_player <= self.enemy.config['attack_range']:
            self.state = 'attack'
            self.perform_attack()
        elif distance_to_player <= self.enemy.config['detection_range']:
            if self.enemy.health < self.enemy.config['health'] * 0.3:
                self.state = 'defensive'
                self.defensive_behavior(dt)
            else:
                self.state = 'chase'
                self.update_path_to_player()
                self.follow_path(dt)
        else:
            self.state = 'idle'
            self.patrol(dt)

    def update_boss_behavior(self, dt):
        # Get current phase based on health percentage
        health_percentage = self.enemy.health / self.enemy.config['health']
        current_phase = None
        
        for phase in self.enemy.config['phases']:
            if health_percentage <= phase['health_threshold']:
                current_phase = phase
                break
        
        if current_phase:
            if current_phase['attack_pattern'] == 'aggressive':
                self.aggressive_behavior(dt)
            elif current_phase['attack_pattern'] == 'defensive':
                self.defensive_behavior(dt)
            elif current_phase['attack_pattern'] == 'berserk':
                self.berserk_behavior(dt)

    def aggressive_behavior(self, dt):
        distance_to_player = (self.enemy.player.position - self.enemy.position).length()
        
        if distance_to_player <= self.enemy.config['attacks']['charge']['range']:
            self.perform_charge_attack()
        elif distance_to_player <= self.enemy.config['attacks']['melee']['range']:
            self.perform_melee_attack()
        else:
            self.update_path_to_player()
            self.follow_path(dt)

    def defensive_behavior(self, dt):
        distance_to_player = (self.enemy.player.position - self.enemy.position).length()
        
        if distance_to_player < self.enemy.config['attack_range']:
            self.retreat_from_player(dt)
        else:
            self.perform_ranged_attack()

    def berserk_behavior(self, dt):
        # Increased speed and aggression
        self.enemy.speed = self.enemy.config['speed'] * 1.5
        
        distance_to_player = (self.enemy.player.position - self.enemy.position).length()
        
        if distance_to_player <= self.enemy.config['attacks']['slam']['range']:
            self.perform_slam_attack()
        else:
            self.perform_charge_attack()

    def update_path_to_player(self):
        current_time = time.time()
        if current_time - self.last_path_update >= self.path_update_interval:
            self.path = self.enemy.nav_mesh.find_path(
                self.enemy.position,
                self.enemy.player.position
            )
            self.next_waypoint = 0
            self.last_path_update = current_time

    def follow_path(self, dt):
        if not self.path or self.next_waypoint >= len(self.path):
            return
            
        # Move towards next waypoint
        target = self.path[self.next_waypoint]
        direction = (target - self.enemy.position).normalized()
        self.enemy.position += direction * self.enemy.speed * dt
        
        # Look at movement direction
        self.enemy.look_at_2d(self.enemy.position + direction)
        
        # Check if reached waypoint
        if (target - self.enemy.position).length() < 0.5:
            self.next_waypoint += 1

    def patrol(self, dt):
        if not hasattr(self, 'patrol_point') or \
           (self.patrol_point - self.enemy.position).length() < 1:
            # Generate new patrol point
            angle = random.uniform(0, math.tau)
            distance = random.uniform(5, 10)
            self.patrol_point = self.enemy.position + Vec3(
                math.cos(angle) * distance,
                0,
                math.sin(angle) * distance
            )
        
        # Move towards patrol point
        direction = (self.patrol_point - self.enemy.position).normalized()
        self.enemy.position += direction * self.enemy.speed * 0.5 * dt
        self.enemy.look_at_2d(self.enemy.position + direction)

    def retreat_from_player(self, dt):
        direction = (self.enemy.position - self.enemy.player.position).normalized()
        retreat_pos = self.enemy.position + direction * 5
        
        # Check if retreat position is valid
        if self.enemy.nav_mesh.is_position_valid(retreat_pos):
            self.enemy.position += direction * self.enemy.speed * dt
            self.enemy.look_at_2d(self.enemy.player.position)

    def find_shooting_position(self, dt):
        if not hasattr(self, 'shooting_position') or \
           (self.shooting_position - self.enemy.position).length() < 1:
            # Generate new shooting position
            angle = random.uniform(0, math.tau)
            distance = random.uniform(5, 10)
            self.shooting_position = self.enemy.position + Vec3(
                math.cos(angle) * distance,
                0,
                math.sin(angle) * distance
            )
        
        # Move towards shooting position
        direction = (self.shooting_position - self.enemy.position).normalized()
        self.enemy.position += direction * self.enemy.speed * 0.5 * dt
        self.enemy.look_at_2d(self.enemy.position + direction)

    def perform_attack(self):
        # Implement attack logic
        pass

    def perform_ranged_attack(self):
        # Implement ranged attack logic
        pass

    def perform_charge_attack(self):
        # Implement charge attack logic
        pass

    def perform_melee_attack(self):
        # Implement melee attack logic
        pass

    def perform_slam_attack(self):
        # Implement slam attack logic
        pass

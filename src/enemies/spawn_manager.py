from ursina import *
from src.enemies.enemy_base import EnemyBase
from src.config.enemy_config import SPAWN_CONFIG
import random
import math

class SpawnManager:
    def __init__(self, player, nav_mesh):
        self.player = player
        self.nav_mesh = nav_mesh
        self.active_enemies = []
        self.last_spawn_time = 0
        self.game_time = 0
        
    def update(self):
        current_time = time.time()
        self.game_time += time.dt
        
        # Clean up dead enemies
        self.active_enemies = [e for e in self.active_enemies if e.enabled]
        
        # Check if we can spawn more enemies
        if (len(self.active_enemies) < SPAWN_CONFIG['max_enemies'] and
            current_time - self.last_spawn_time >= SPAWN_CONFIG['spawn_cooldown']):
            self.spawn_enemy()

    def spawn_enemy(self):
        # Choose random enemy type
        enemy_type = random.choice(list(ENEMY_TYPES.keys()))
        
        # Find valid spawn position
        spawn_pos = self.find_spawn_position()
        if not spawn_pos:
            return
            
        # Create enemy
        enemy = EnemyBase(enemy_type, self.player, self.nav_mesh)
        enemy.position = spawn_pos
        
        # Apply difficulty scaling
        minutes_passed = self.game_time / 60
        stat_multiplier = 1 + (minutes_passed * SPAWN_CONFIG['difficulty_scaling'])
        
        enemy.health *= stat_multiplier
        enemy.damage *= stat_multiplier
        enemy.speed *= stat_multiplier
        
        self.active_enemies.append(enemy)
        self.last_spawn_time = time.time()

    def find_spawn_position(self):
        for _ in range(10):  # Try 10 times to find valid position
            # Generate random angle and distance
            angle = random.uniform(0, math.tau)
            distance = random.uniform(
                SPAWN_CONFIG['spawn_distance'],
                SPAWN_CONFIG['spawn_distance'] * 1.5
            )
            
            # Calculate position
            pos = Vec3(
                self.player.x + math.cos(angle) * distance,
                0,
                self.player.z + math.sin(angle) * distance
            )
            
            # Check if position is valid (not inside obstacles)
            if self.is_valid_spawn_position(pos):
                return pos
                
        return None

    def is_valid_spawn_position(self, position):
        # Check if position is on navmesh
        grid_x, grid_z = self.nav_mesh.world_to_grid(position)
        if self.nav_mesh.grid_data[grid_x, grid_z] == 0:
            return False
            
        # Check if there's a path to player
        path = self.nav_mesh.find_path(position, self.player.position)
        return len(path) > 0

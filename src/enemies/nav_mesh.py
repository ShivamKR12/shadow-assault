from ursina import *
import numpy as np
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class NavMesh:
    def __init__(self, level_size=100, cell_size=1):
        self.level_size = level_size
        self.cell_size = cell_size
        self.grid_size = int(level_size / cell_size)
        self.grid_data = np.ones((self.grid_size, self.grid_size), dtype=int)
        self.finder = AStarFinder()
        
    def update_grid(self, level_entities):
        # Reset grid
        self.grid_data.fill(1)
        
        # Mark obstacles in grid
        for entity in level_entities:
            if hasattr(entity, 'collider') and entity.collider:
                # Convert world position to grid coordinates
                grid_x = int((entity.x + self.level_size/2) / self.cell_size)
                grid_z = int((entity.z + self.level_size/2) / self.cell_size)
                
                # Mark area as obstacle
                size_x = int(entity.scale_x / self.cell_size)
                size_z = int(entity.scale_z / self.cell_size)
                
                for x in range(max(0, grid_x - size_x), min(self.grid_size, grid_x + size_x)):
                    for z in range(max(0, grid_z - size_z), min(self.grid_size, grid_z + size_z)):
                        self.grid_data[x, z] = 0

    def world_to_grid(self, position):
        x = int((position.x + self.level_size/2) / self.cell_size)
        z = int((position.z + self.level_size/2) / self.cell_size)
        return max(0, min(x, self.grid_size-1)), max(0, min(z, self.grid_size-1))

    def grid_to_world(self, grid_x, grid_z):
        x = (grid_x * self.cell_size) - (self.level_size/2)
        z = (grid_z * self.cell_size) - (self.level_size/2)
        return Vec3(x, 0, z)

    def find_path(self, start_pos, end_pos):
        # Convert world positions to grid coordinates
        start_x, start_z = self.world_to_grid(start_pos)
        end_x, end_z = self.world_to_grid(end_pos)
        
        # Create grid for pathfinding
        grid = Grid(matrix=self.grid_data)
        start = grid.node(start_x, start_z)
        end = grid.node(end_x, end_z)
        
        # Find path
        path, _ = self.finder.find_path(start, end, grid)
        
        # Convert path back to world coordinates
        return [self.grid_to_world(x, y) for x, y in path]

from ursina import *
import numpy as np

class CollisionSystem:
    def __init__(self):
        self.collision_margin = 0.1
        self.slope_limit = 45  # Maximum slope angle in degrees
        
    def check_collision(self, entity, direction, dt):
        """Advanced collision detection with slope handling"""
        original_pos = entity.position
        target_pos = original_pos + direction * dt
        
        # Cast multiple rays for better precision
        collision_points = self.cast_collision_rays(entity, target_pos)
        
        if not collision_points:
            return target_pos, None
            
        # Find the nearest collision point
        nearest_point = min(collision_points, key=lambda x: (x[0] - original_pos).length())
        hit_point, hit_normal = nearest_point
        
        # Handle slopes
        if hit_normal.y > 0:  # If hitting a slope
            slope_angle = degrees(acos(hit_normal.y))
            
            if slope_angle <= self.slope_limit:
                # Calculate slide vector along slope
                slide_vec = self.calculate_slide_vector(direction, hit_normal)
                return original_pos + slide_vec * dt, hit_normal
                
        # Return collision position and normal
        return hit_point + hit_normal * self.collision_margin, hit_normal

    def cast_collision_rays(self, entity, target_pos):
        """Cast multiple rays for precise collision detection"""
        collision_points = []
        ray_origins = self.get_ray_origins(entity)
        
        for origin in ray_origins:
            ray_dir = (target_pos - origin).normalized()
            hit_info = raycast(
                origin=origin,
                direction=ray_dir,
                distance=entity.scale_y,
                ignore=[entity]
            )
            
            if hit_info.hit:
                collision_points.append((hit_info.point, hit_info.normal))
                
        return collision_points

    def get_ray_origins(self, entity):
        """Get multiple ray origin points around the entity"""
        origins = []
        height = entity.scale_y
        radius = entity.scale_x * 0.5
        
        # Center ray
        origins.append(entity.position)
        
        # Corner rays
        for x in [-radius, radius]:
            for z in [-radius, radius]:
                origins.append(entity.position + Vec3(x, 0, z))
                origins.append(entity.position + Vec3(x, height * 0.5, z))
                
        return origins

    def calculate_slide_vector(self, direction, normal):
        """Calculate sliding vector along a slope"""
        return direction - normal * direction.dot(normal)

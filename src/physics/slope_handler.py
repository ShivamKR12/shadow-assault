from ursina import *
import math

class SlopeHandler:
    def __init__(self):
        self.max_slope_angle = 45  # Maximum walkable slope angle
        self.step_height = 0.3     # Maximum step height player can climb
        self.gravity = 9.81
        
    def handle_slope(self, entity, velocity, dt):
        """Handle slope movement and stepping"""
        # Ground check ray
        ground_hit = raycast(
            origin=entity.position + Vec3(0, 0.1, 0),
            direction=Vec3(0, -1, 0),
            distance=1.1,
            ignore=[entity]
        )
        
        if ground_hit.hit:
            slope_angle = degrees(acos(ground_hit.normal.y))
            
            if slope_angle <= self.max_slope_angle:
                # Adjust position to slope
                target_y = ground_hit.point.y + entity.scale_y * 0.5
                entity.y = lerp(entity.y, target_y, dt * 10)
                
                # Adjust velocity for slope
                if slope_angle > 5:  # Slight slopes don't need velocity adjustment
                    slope_factor = 1.0 - (slope_angle / self.max_slope_angle) * 0.5
                    velocity.xz *= slope_factor
                    
                    # Add downhill acceleration on steep slopes
                    if slope_angle > 30:
                        downhill_dir = Vec3(
                            ground_hit.normal.x,
                            0,
                            ground_hit.normal.z
                        ).normalized()
                        velocity += downhill_dir * self.gravity * dt * (slope_angle / self.max_slope_angle)
            
            # Handle steps
            if slope_angle > self.max_slope_angle:
                step_hit = raycast(
                    origin=entity.position + Vec3(0, self.step_height, 0),
                    direction=velocity.normalized(),
                    distance=0.5,
                    ignore=[entity]
                )
                
                if not step_hit.hit:
                    entity.y += self.step_height
                    
        return velocity

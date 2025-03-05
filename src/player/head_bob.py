from ursina import *
import math

class HeadBob:
    def __init__(self, camera):
        self.camera = camera
        
        # Bob parameters
        self.bob_amplitude = Vec3(0.08, 0.08, 0.08)  # X, Y, Z amplitude
        self.bob_frequency = Vec3(4.0, 2.0, 4.0)     # X, Y, Z frequency
        self.bob_running_multiplier = 1.5
        
        # State
        self.bob_time = 0
        self.target_bob = Vec3(0, 0, 0)
        self.current_bob = Vec3(0, 0, 0)
        self.smoothing = 10
        self.original_position = camera.position

    def update(self, dt, velocity, running, grounded):
        if not grounded:
            # Smoothly return to center when in air
            self.target_bob = Vec3(0, 0, 0)
        else:
            # Calculate bob based on movement speed
            speed = velocity.xz.length()
            
            if speed > 0.1:  # Only bob when moving
                # Increase time based on speed
                self.bob_time += dt * speed * (
                    self.bob_running_multiplier if running else 1.0
                )
                
                # Calculate bob offset
                self.target_bob = Vec3(
                    math.sin(self.bob_time * self.bob_frequency.x) * self.bob_amplitude.x,
                    math.sin(self.bob_time * self.bob_frequency.y) * self.bob_amplitude.y,
                    math.sin(self.bob_time * self.bob_frequency.z) * self.bob_amplitude.z
                )
                
                # Adjust amplitude based on speed
                self.target_bob *= min(speed / 5.0, 1.0)
                
                # Increase bob when running
                if running:
                    self.target_bob *= self.bob_running_multiplier
            else:
                self.target_bob = Vec3(0, 0, 0)

        # Smoothly interpolate current bob
        self.current_bob = lerp(
            self.current_bob,
            self.target_bob,
            dt * self.smoothing
        )
        
        # Apply bob to camera
        self.camera.position = self.original_position + self.current_bob

    def reset(self):
        """Reset head bob to center"""
        self.bob_time = 0
        self.target_bob = Vec3(0, 0, 0)
        self.current_bob = Vec3(0, 0, 0)
        self.camera.position = self.original_position

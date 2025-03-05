from ursina import *
import random

class FootstepSystem:
    def __init__(self, player):
        self.player = player
        self.step_distance = 0
        self.step_interval = 2.0  # Distance between footsteps
        self.last_position = player.position
        
        # Load footstep sounds for different surfaces
        self.footstep_sounds = {
            'concrete': [
                Audio('assets/sounds/footsteps/concrete1.wav', autoplay=False),
                Audio('assets/sounds/footsteps/concrete2.wav', autoplay=False),
                Audio('assets/sounds/footsteps/concrete3.wav', autoplay=False)
            ],
            'metal': [
                Audio('assets/sounds/footsteps/metal1.wav', autoplay=False),
                Audio('assets/sounds/footsteps/metal2.wav', autoplay=False),
                Audio('assets/sounds/footsteps/metal3.wav', autoplay=False)
            ],
            'grass': [
                Audio('assets/sounds/footsteps/grass1.wav', autoplay=False),
                Audio('assets/sounds/footsteps/grass2.wav', autoplay=False),
                Audio('assets/sounds/footsteps/grass3.wav', autoplay=False)
            ]
        }
        
        self.running_interval = 1.2  # Shorter interval for running
        self.volume_range = (0.7, 1.0)

    def update(self):
        if not self.player.grounded:
            return
            
        # Calculate distance moved
        movement = (self.player.position - self.last_position).xz
        self.step_distance += movement.length()
        self.last_position = self.player.position
        
        # Determine step interval based on movement speed
        current_interval = (
            self.running_interval 
            if self.player.running 
            else self.step_interval
        )
        
        # Play footstep sound when interval is reached
        if self.step_distance >= current_interval:
            self.play_footstep()
            self.step_distance = 0

    def play_footstep(self):
        # Detect surface type
        surface = self.detect_surface()
        
        if surface in self.footstep_sounds:
            # Select random footstep sound for variety
            sound = random.choice(self.footstep_sounds[surface])
            
            # Randomize volume slightly
            volume = random.uniform(*self.volume_range)
            
            # Play sound
            sound.volume = volume
            sound.play()

    def detect_surface(self):
        """Detect surface type under player"""
        hit_info = raycast(
            origin=self.player.position + Vec3(0, 0.1, 0),
            direction=Vec3(0, -1, 0),
            distance=1.1,
            ignore=[self.player]
        )
        
        if hit_info.hit:
            # Check surface material tag or texture
            if hasattr(hit_info.entity, 'surface_type'):
                return hit_info.entity.surface_type
                
        return 'concrete'  # Default surface type

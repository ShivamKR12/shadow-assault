from ursina import *
import random

class ParticleSystem:
    def __init__(self):
        self.active_particles = []

    def create_impact_effect(self, position, normal, color=color.white):
        num_particles = 20
        
        for _ in range(num_particles):
            # Calculate random spread
            spread = Vec3(
                random.uniform(-0.5, 0.5),
                random.uniform(-0.5, 0.5),
                random.uniform(-0.5, 0.5)
            ).normalized()
            
            # Create particle
            particle = Entity(
                model='sphere',
                scale=0.05,
                color=color,
                position=position,
                collision=False
            )
            
            # Calculate velocity
            velocity = (normal + spread) * random.uniform(3, 5)
            
            # Animate position
            particle.animate_position(
                particle.position + velocity,
                duration=0.5,
                curve=curve.out_expo
            )
            
            # Fade out
            particle.animate_scale(0, duration=0.5)
            particle.animate_color(color.rgba(0,0,0,0), duration=0.5)
            
            # Destroy after animation
            destroy(particle, delay=0.5)
            
            self.active_particles.append(particle)

    def create_muzzle_flash(self, position, direction):
        # Create light flash
        flash = PointLight(
            parent=camera,
            position=position,
            color=color.yellow,
            range=10
        )
        
        # Animate light
        flash.animate_color(color.black, duration=0.1)
        destroy(flash, delay=0.1)
        
        # Create particles
        num_particles = 10
        for _ in range(num_particles):
            spread = Vec3(
                random.uniform(-0.2, 0.2),
                random.uniform(-0.2, 0.2),
                random.uniform(-0.2, 0.2)
            )
            
            particle = Entity(
                model='quad',
                texture='assets/textures/particles/smoke.png',
                position=position,
                scale=0.1,
                color=color.white50,
                billboard=True
            )
            
            # Animate particle
            end_pos = position + (direction + spread) * random.uniform(0.5, 1)
            particle.animate_position(end_pos, duration=0.2)
            particle.animate_scale(0.3, duration=0.2)
            particle.animate_color(color.clear, duration=0.2)
            
            destroy(particle, delay=0.2)

from ursina import *
import random
import math

class AdvancedParticleSystem:
    def __init__(self):
        self.active_particles = []
        
    def create_explosion(self, position, scale=1.0, color=color.yellow):
        num_particles = int(30 * scale)
        
        # Create light flash
        flash = PointLight(
            position=position,
            color=color,
            range=10 * scale
        )
        flash.animate_color(color.black, duration=0.2)
        destroy(flash, delay=0.2)
        
        # Create shockwave
        shockwave = Entity(
            model='sphere',
            position=position,
            scale=0.1,
            color=color.rgba(1, 1, 1, 0.5)
        )
        shockwave.animate_scale(5 * scale, duration=0.5)
        shockwave.animate_color(color.rgba(1, 1, 1, 0), duration=0.5)
        destroy(shockwave, delay=0.5)
        
        # Create particles
        for _ in range(num_particles):
            angle = random.uniform(0, math.tau)
            height = random.uniform(0.2, 1.0)
            speed = random.uniform(3, 6) * scale
            
            particle = Entity(
                model='sphere',
                position=position,
                scale=0.1 * scale,
                color=color
            )
            
            end_pos = position + Vec3(
                math.cos(angle) * speed,
                height * speed,
                math.sin(angle) * speed
            )
            
            particle.animate_position(end_pos, duration=1, curve=curve.out_expo)
            particle.animate_scale(0, duration=1)
            particle.animate_color(color.rgba(0,0,0,0), duration=1)
            destroy(particle, delay=1)

    def create_trail(self, entity, color=color.white50):
        def update_trail():
            particle = Entity(
                model='quad',
                texture='assets/textures/particles/trail.png',
                position=entity.position,
                scale=0.2,
                color=color,
                billboard=True
            )
            particle.animate_scale(0, duration=0.5)
            particle.animate_color(color.clear, duration=0.5)
            destroy(particle, delay=0.5)
            
        return update_trail

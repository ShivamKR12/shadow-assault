from ursina import *

class WeaponAnimator:
    def __init__(self, weapon):
        self.weapon = weapon
        self.animations = {}
        self.current_animation = None
        self.load_animations()

    def load_animations(self):
        for anim_name, anim_path in self.weapon.config['animations'].items():
            self.animations[anim_name] = Animation(
                anim_path,
                loop=False,
                autoplay=False
            )

    def play(self, animation_name):
        if animation_name in self.animations:
            if self.current_animation:
                self.current_animation.pause()
            
            self.current_animation = self.animations[animation_name]
            self.current_animation.start()

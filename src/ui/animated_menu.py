from ursina import *
from src.config.ui_config import UI_CONFIG

class AnimatedMenu(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        self.elements = []
        self.animation_time = 0.3

    def add_element(self, element, start_position, end_position):
        element.original_position = end_position
        element.position = start_position
        self.elements.append(element)

    def show_animated(self):
        for i, element in enumerate(self.elements):
            element.position = element.original_position + Vec3(0, -1, 0)
            element.alpha = 0
            
            element.animate_position(
                element.original_position,
                duration=self.animation_time,
                delay=i * 0.1,
                curve=curve.out_expo
            )
            
            element.animate('alpha', 1, 
                duration=self.animation_time,
                delay=i * 0.1,
                curve=curve.linear
            )

    def hide_animated(self):
        for i, element in enumerate(self.elements):
            element.animate_position(
                element.position + Vec3(0, 1, 0),
                duration=self.animation_time,
                delay=i * 0.05,
                curve=curve.in_expo
            )
            
            element.animate('alpha', 0,
                duration=self.animation_time,
                delay=i * 0.05,
                curve=curve.linear
            )

from ursina import *

class BasicLevel:
    def __init__(self):
        self.entities = []
        self.create_test_level()

    def create_test_level(self):
        # Create boxes for testing collision
        box_positions = [
            (5, 1, 5),
            (-5, 1, -5),
            (0, 1, 10),
            (10, 1, 0),
        ]

        for pos in box_positions:
            box = Entity(
                model='cube',
                position=pos,
                scale=(2, 2, 2),
                texture='white_cube',
                color=color.orange,
                collider='box'
            )
            self.entities.append(box)

        # Create platforms
        platform_data = [
            ((0, 3, -8), (6, 0.5, 2)),   # (position, scale)
            ((8, 5, 0), (2, 0.5, 6)),
            ((-8, 2, 4), (4, 0.5, 4)),
        ]

        for pos, scale in platform_data:
            platform = Entity(
                model='cube',
                position=pos,
                scale=scale,
                texture='white_cube',
                color=color.gray,
                collider='box'
            )
            self.entities.append(platform)

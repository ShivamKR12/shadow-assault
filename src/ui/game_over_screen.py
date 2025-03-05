from ursina import *
from src.ui.animated_menu import AnimatedMenu

class GameOverScreen(AnimatedMenu):
    def __init__(self, score, is_victory=False):
        super().__init__()
        
        # Title
        self.title = Text(
            text='VICTORY!' if is_victory else 'GAME OVER',
            scale=4,
            color=color.green if is_victory else color.red
        )
        self.add_element(self.title, Vec3(0, 0.3, 0), Vec3(0, 0.3, 0))
        
        # Score
        self.score_text = Text(
            text=f'Final Score: {score}',
            scale=2
        )
        self.add_element(self.score_text, Vec3(0, 0.1, 0), Vec3(0, 0.1, 0))
        
        # Buttons
        self.retry_button = Button(
            text='Try Again',
            scale=(0.3, 0.08),
            color=color.azure
        )
        self.add_element(self.retry_button, Vec3(0, -0.1, 0), Vec3(0, -0.1, 0))
        
        self.menu_button = Button(
            text='Main Menu',
            scale=(0.3, 0.08),
            color=color.azure
        )
        self.add_element(self.menu_button, Vec3(0, -0.2, 0), Vec3(0, -0.2, 0))

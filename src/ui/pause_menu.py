from ursina import *
from src.config.ui_config import UI_CONFIG, SOUND_CONFIG

class PauseMenu(Entity):
    def __init__(self, resume_callback, quit_callback):
        super().__init__(parent=camera.ui)
        self.resume_callback = resume_callback
        self.quit_callback = quit_callback
        
        # Create semi-transparent background
        self.background = Entity(
            parent=self,
            model='quad',
            scale=(2, 1),
            color=UI_CONFIG['colors']['background']
        )
        
        # Create pause menu text
        self.title = Text(
            parent=self,
            text='PAUSED',
            scale=3,
            origin=(0, 0),
            y=0.2
        )
        
        # Create buttons
        self.buttons = {
            'resume': Button(
                parent=self,
                text='Resume',
                scale=(0.3, 0.08),
                y=0.05,
                color=UI_CONFIG['colors']['primary']
            ),
            'options': Button(
                parent=self,
                text='Options',
                scale=(0.3, 0.08),
                y=-0.05,
                color=UI_CONFIG['colors']['primary']
            ),
            'quit': Button(
                parent=self,
                text='Quit to Menu',
                scale=(0.3, 0.08),
                y=-0.15,
                color=UI_CONFIG['colors']['primary']
            )
        }
        
        # Setup button callbacks
        self.buttons['resume'].on_click = self.resume_game
        self.buttons['options'].on_click = self.show_options
        self.buttons['quit'].on_click = self.quit_to_menu
        
        # Initially disabled
        self.disable()

    def resume_game(self):
        Audio(SOUND_CONFIG['sounds']['menu_click'], volume=SOUND_CONFIG['sfx_volume'])
        self.disable()
        self.resume_callback()

    def quit_to_menu(self):
        Audio(SOUND_CONFIG['sounds']['menu_click'], volume=SOUND_CONFIG['sfx_volume'])
        self.disable()
        self.quit_callback()

    def show_options(self):
        Audio(SOUND_CONFIG['sounds']['menu_click'], volume=SOUND_CONFIG['sfx_volume'])
        # Implement options menu
        pass

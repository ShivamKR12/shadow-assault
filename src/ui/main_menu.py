from ursina import *
from src.config.ui_config import UI_CONFIG, SOUND_CONFIG

class MainMenu(Entity):
    def __init__(self, start_game_callback):
        super().__init__(parent=camera.ui)
        self.start_game_callback = start_game_callback
        
        # Background
        self.background = Entity(
            parent=self,
            model='quad',
            texture='assets/textures/ui/menu_background.png',
            scale=(2, 1),
            color=color.rgb(50, 50, 50)
        )
        
        # Title
        self.title = Text(
            parent=self,
            text='FPS GAME',
            scale=4,
            origin=(0, 0),
            y=0.3
        )
        
        # Create buttons
        self.buttons = {
            'start': Button(
                parent=self,
                text='Start Game',
                scale=(0.3, 0.08),
                y=0.1,
                color=UI_CONFIG['colors']['primary']
            ),
            'options': Button(
                parent=self,
                text='Options',
                scale=(0.3, 0.08),
                y=0,
                color=UI_CONFIG['colors']['primary']
            ),
            'quit': Button(
                parent=self,
                text='Quit',
                scale=(0.3, 0.08),
                y=-0.1,
                color=UI_CONFIG['colors']['primary']
            )
        }
        
        # Setup button callbacks
        self.buttons['start'].on_click = self.start_game
        self.buttons['options'].on_click = self.show_options
        self.buttons['quit'].on_click = application.quit
        
        # Setup hover sounds
        for button in self.buttons.values():
            button.original_color = button.color
            button.highlight_color = UI_CONFIG['colors']['secondary']
            
            def hover_sound():
                Audio(SOUND_CONFIG['sounds']['menu_hover'], volume=SOUND_CONFIG['sfx_volume'])
            
            button.on_mouse_enter = hover_sound

    def start_game(self):
        Audio(SOUND_CONFIG['sounds']['game_start'], volume=SOUND_CONFIG['sfx_volume'])
        self.disable()
        self.start_game_callback()

    def show_options(self):
        Audio(SOUND_CONFIG['sounds']['menu_click'], volume=SOUND_CONFIG['sfx_volume'])
        # Implement options menu
        pass

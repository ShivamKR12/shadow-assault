from ursina import *
from src.config.ui_config import UI_CONFIG

class HUD(Entity):
    def __init__(self, player):
        super().__init__(parent=camera.ui)
        self.player = player
        
        # Create health bar
        self.health_bar_bg = Entity(
            parent=self,
            model='quad',
            scale=UI_CONFIG['hud']['health_bar_size'],
            position=UI_CONFIG['hud']['health_bar_position'],
            color=color.dark_gray
        )
        
        self.health_bar = Entity(
            parent=self.health_bar_bg,
            model='quad',
            scale=(1, 1),
            scale_x=1,
            position=(0, 0),
            origin=(-0.5, 0),
            color=UI_CONFIG['colors']['success']
        )
        
        # Create ammo counter
        self.ammo_text = Text(
            parent=self,
            text='30/30',
            position=UI_CONFIG['hud']['ammo_position'],
            scale=2
        )
        
        # Create score display
        self.score_text = Text(
            parent=self,
            text='Score: 0',
            position=UI_CONFIG['hud']['score_position'],
            scale=1.5
        )
        
        # Create crosshair
        self.crosshair = Entity(
            parent=self,
            model='quad',
            scale=UI_CONFIG['hud']['crosshair_size'],
            color=UI_CONFIG['colors']['text'],
            rotation_z=45
        )

    def update(self):
        # Update health bar
        health_percentage = self.player.health / self.player.max_health
        self.health_bar.scale_x = health_percentage
        self.health_bar.color = color.lerp(
            UI_CONFIG['colors']['danger'],
            UI_CONFIG['colors']['success'],
            health_percentage
        )
        
        # Update ammo counter
        if hasattr(self.player, 'weapon_manager'):
            weapon = self.player.weapon_manager.current_weapon
            if weapon:
                self.ammo_text.text = f'{weapon.ammo}/{weapon.max_ammo}'
        
        # Update score
        if hasattr(self.player, 'score'):
            self.score_text.text = f'Score: {self.player.score}'

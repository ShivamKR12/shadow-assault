import sys
from pathlib import Path
from ursina import *
from src.ui.hud import HUD
from src.ui.main_menu import MainMenu
from src.ui.pause_menu import PauseMenu
from src.effects.particle_system import ParticleSystem
from src.effects.advanced_particle_system import AdvancedParticleSystem
from src.utils.settings_manager import SettingsManager
from src.ui.loading_screen import LoadingScreen
from src.ui.game_over_screen import GameOverScreen
from src.ui.tutorial_system import TutorialSystem
from src.utils.leaderboard import Leaderboard
from src.utils.achievement_system import AchievementSystem

# Add the parent directory of src to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

app = Ursina()

class Game():
    def __init__(self):
        super().__init__()
        self.particle_system = ParticleSystem()
        self.advanced_particle_system = AdvancedParticleSystem()
        self.settings_manager = SettingsManager()
        self.leaderboard = Leaderboard()
        self.achievement_system = AchievementSystem()
        self.tutorial_system = TutorialSystem()
        self.setup_game()

    def setup_game(self):
        # Create UI elements
        self.main_menu = MainMenu(self.start_game)
        self.pause_menu = PauseMenu(self.resume_game, self.quit_to_menu)
        self.hud = HUD(self.player)
        self.hud.disable()  # Start with HUD disabled
        self.loading_screen = LoadingScreen()
        
        # Game state
        self.paused = False
        mouse.locked = False

    def start_game(self):
        mouse.locked = True
        self.hud.enable()
        # Initialize game elements
        self.loading_screen.update_progress(1.0)
        self.loading_screen.finish_loading()

    def resume_game(self):
        self.paused = False
        mouse.locked = True

    def pause_game(self):
        self.paused = True
        mouse.locked = False
        self.pause_menu.enable()

    def quit_to_menu(self):
        # Clean up game state
        self.player.position = Vec3(0, 0, 0)
        mouse.locked = False
        self.hud.disable()
        self.main_menu.enable()

    def input(self, key):
        if key == 'escape':
            if not self.main_menu.enabled:
                if self.paused:
                    self.resume_game()
                    self.pause_menu.disable()
                else:
                    self.pause_game()

    def update(self):
        if not self.paused and not self.main_menu.enabled:
            # Update game logic
            self.player.update()
            self.tutorial_system.update()
            self.hud.update()
            self.achievement_system.update()
            self.particle_system.update()
            self.advanced_particle_system.update()
            
            # Check for game over conditions
            if self.player.health <= 0:
                self.end_game(victory=False)

    def end_game(self, victory):
        self.paused = True
        mouse.locked = False
        self.hud.disable()
        self.game_over_screen = GameOverScreen(score=self.player.score, is_victory=victory)
        self.game_over_screen.enable()

if __name__ == '__main__':
    app.run()
from ursina import *

class LoadingScreen(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        
        # Background
        self.background = Entity(
            parent=self,
            model='quad',
            texture='assets/textures/ui/loading_background.png',
            scale=(2, 1),
            color=color.black
        )
        
        # Loading bar background
        self.bar_bg = Entity(
            parent=self,
            model='quad',
            scale=(0.7, 0.05),
            position=(0, -0.2),
            color=color.dark_gray
        )
        
        # Loading bar progress
        self.bar = Entity(
            parent=self.bar_bg,
            model='quad',
            scale=(0, 1),
            origin=(-0.5, 0),
            color=color.azure
        )
        
        # Loading text
        self.text = Text(
            parent=self,
            text='Loading...',
            position=(0, -0.3),
            origin=(0, 0),
            scale=2
        )
        
        self.tips = [
            "Press 'R' to reload your weapon!",
            "Headshots deal extra damage!",
            "Keep moving to avoid enemy fire!",
        ]
        
        self.tip_text = Text(
            parent=self,
            text=random.choice(self.tips),
            position=(0, -0.4),
            origin=(0, 0),
            scale=1.5,
            color=color.light_gray
        )

    def update_progress(self, progress):
        self.bar.scale_x = progress
        if progress >= 1:
            self.finish_loading()

    def finish_loading(self):
        self.animate_out()

    def animate_out(self):
        self.animate('alpha', 0, duration=0.5)
        destroy(self, delay=0.5)

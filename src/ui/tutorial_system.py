from ursina import *

class TutorialSystem:
    def __init__(self):
        self.tutorials = {
            'movement': {
                'text': 'Use WASD to move',
                'position': Vec2(0, 0.3),
                'trigger': 'game_start'
            },
            'shooting': {
                'text': 'Left Click to shoot',
                'position': Vec2(0, 0.2),
                'trigger': 'first_enemy'
            },
            'reload': {
                'text': 'Press R to reload',
                'position': Vec2(0, 0.1),
                'trigger': 'low_ammo'
            }
        }
        
        self.active_tutorials = {}
        
    def show_tutorial(self, tutorial_id):
        if tutorial_id not in self.tutorials:
            return
            
        tutorial = self.tutorials[tutorial_id]
        
        # Create tutorial text
        text = Text(
            text=tutorial['text'],
            position=tutorial['position'],
            scale=2,
            origin=(0, 0),
            color=color.white
        )
        
        # Add background panel
        panel = Entity(
            parent=text,
            model='quad',
            scale=(text.width + 0.1, text.height + 0.1),
            color=color.black66,
            z=0.1
        )
        
        # Store active tutorial
        self.active_tutorials[tutorial_id] = (text, panel)
        
        # Animate in
        text.alpha = 0
        panel.alpha = 0
        text.animate('alpha', 1, duration=0.3)
        panel.animate('alpha', 0.66, duration=0.3)
        
    def hide_tutorial(self, tutorial_id):
        if tutorial_id not in self.active_tutorials:
            return
            
        text, panel = self.active_tutorials[tutorial_id]
        
        # Animate out
        text.animate('alpha', 0, duration=0.3)
        panel.animate('alpha', 0, duration=0.3)
        
        # Cleanup
        destroy(text, delay=0.3)
        destroy(panel, delay=0.3)
        del self.active_tutorials[tutorial_id]

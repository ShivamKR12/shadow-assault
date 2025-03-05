from ursina import *

class AchievementSystem:
    def __init__(self):
        self.achievements = {
            'first_kill': {
                'name': 'First Blood',
                'description': 'Kill your first enemy',
                'icon': 'assets/textures/achievements/first_kill.png'
            },
            'sharpshooter': {
                'name': 'Sharpshooter',
                'description': 'Get 10 headshots',
                'icon': 'assets/textures/achievements/headshot.png'
            },
            'survivor': {
                'name': 'Survivor',
                'description': 'Survive for 5 minutes',
                'icon': 'assets/textures/achievements/survivor.png'
            }
        }
        
        self.unlocked_achievements = set()
        self.notification_queue = []
        self.current_notification = None

    def unlock_achievement(self, achievement_id):
        if achievement_id not in self.achievements or achievement_id in self.unlocked_achievements:
            return
            
        self.unlocked_achievements.add(achievement_id)
        self.show_notification(achievement_id)
        self.save_achievements()

    def show_notification(self, achievement_id):
        achievement = self.achievements[achievement_id]
        
        # Create notification entity
        notification = Entity(
            parent=camera.ui,
            position=Vec3(0.7, 0.4, 0),
            scale=(0.4, 0.1)
        )
        
        # Background
        background = Entity(
            parent=notification,
            model='quad',
            color=color.black66,
            scale=(1, 1)
        )
        
        # Icon
        icon = Entity(
            parent=notification,
            model='quad',
            texture=achievement['icon'],
            scale=(0.1, 0.1),
            position=(-0.4, 0, 0)
        )
        
        # Text
        title = Text(
            parent=notification,
            text=achievement['name'],
            position=(-0.3, 0.02),
            scale=1.2
        )
        
        description = Text(
            parent=notification,
            text=achievement['description'],
            position=(-0.3, -0.02),
            scale=0.8
        )
        
        self.notification_queue.append(notification)
        
        if self.current_notification is None:
            self.display_next_notification()

    def display_next_notification(self):
        if not self.notification_queue:
            self.current_notification = None
            return
            
        self.current_notification = self.notification_queue.pop(0)
        self.current_notification.animate('alpha', 1, duration=0.5)
        
        invoke(self.hide_current_notification, delay=3)

    def hide_current_notification(self):
        if self.current_notification:
            self.current_notification.animate('alpha', 0, duration=0.5)
            destroy(self.current_notification, delay=0.5)
            self.current_notification = None
            
        self.display_next_notification()

    def save_achievements(self):
        with open('achievements.json', 'w') as f:
            json.dump(list(self.unlocked_achievements), f)

    def load_achievements(self):
        try:
            with open('achievements.json', 'r') as f:
                self.unlocked_achievements = set(json.load(f))
        except:
            self.unlocked_achievements = set()

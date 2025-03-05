import json
import os

class SettingsManager:
    def __init__(self):
        self.settings_file = 'game_settings.json'
        self.default_settings = {
            'audio': {
                'master_volume': 1.0,
                'music_volume': 0.7,
                'sfx_volume': 0.8
            },
            'graphics': {
                'resolution': '1920x1080',
                'fullscreen': False,
                'vsync': True,
                'quality': 'high'
            },
            'controls': {
                'mouse_sensitivity': 2.0,
                'invert_y': False,
                'key_bindings': {
                    'forward': 'w',
                    'backward': 's',
                    'left': 'a',
                    'right': 'd',
                    'jump': 'space',
                    'reload': 'r'
                }
            }
        }
        self.settings = self.load_settings()

    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            return self.default_settings.copy()
        except:
            return self.default_settings.copy()

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get_setting(self, category, setting):
        return self.settings.get(category, {}).get(setting)

    def set_setting(self, category, setting, value):
        if category not in self.settings:
            self.settings[category] = {}
        self.settings[category][setting] = value
        self.save_settings()

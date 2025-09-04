import json
import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SettingsManager:
    def __init__(self, filepath='json/settings.json'):
        self.filepath = resource_path(filepath)
        self.settings = {
            'volume': 70,
            'grid_color': '#0F82F2'
        }
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                try:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
                except json.JSONDecodeError:
                    print("Warning: Could not read settings.json, using defaults.")
        if hasattr(self, 'sound_manager'):
            self.apply_volume_to_all_sounds()

    def save_settings(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get(self, key):
        return self.settings.get(key)

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()
        if key == 'volume':
            self.apply_volume_to_all_sounds()

    def link_sound_manager(self, sound_manager):
        self.sound_manager = sound_manager
        self.apply_volume_to_all_sounds()

    def apply_volume_to_all_sounds(self):
        if hasattr(self, 'sound_manager') and self.sound_manager:
            volume_float = self.settings.get('volume', 70) / 100.0
            for sound in self.sound_manager.sounds.values():
                sound.setVolume(volume_float)

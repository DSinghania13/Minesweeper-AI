import sys
import os
from PyQt6.QtMultimedia import QSoundEffect, QMediaPlayer, QAudioOutput, QMediaDevices
from PyQt6.QtCore import QUrl


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SoundManager:
    def __init__(self):
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        default_device = QMediaDevices.defaultAudioOutput()
        if not default_device.isNull():
            self.audio_output.setDevice(default_device)

        self.sounds = {
            "start": self._load(resource_path("assets/sounds/start.wav")),
            "click": self._load(resource_path("assets/sounds/click.wav")),
            "flag": self._load(resource_path("assets/sounds/flag.wav")),
            "flag_remove": self._load(resource_path("assets/sounds/flag_remove.wav")),
            "hint": self._load(resource_path("assets/sounds/hint.wav")),
            "bomb": self._load(resource_path("assets/sounds/bomb.wav")),
            "win": self._load(resource_path("assets/sounds/win.wav")),
            "lose": self._load(resource_path("assets/sounds/lose.wav")),
            "hover": self._load(resource_path("assets/sounds/hover.wav")),
            "error": self._load(resource_path("assets/sounds/error.wav")),
        }

    def _load(self, filepath: str) -> QSoundEffect:
        effect = QSoundEffect()
        effect.setSource(QUrl.fromLocalFile(filepath))
        return effect

    def play(self, name: str):
        if name in self.sounds:
            self.sounds[name].play()

    def stop_all(self):
        for name, sound in self.sounds.items():
            if sound.isPlaying():
                print(f"Stopping sound: {name}")
                sound.stop()
                sound.setVolume(0)
                sound.isMuted()
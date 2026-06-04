import sys
import os
import subprocess


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    full_path = os.path.join(base_path, relative_path)

    if not os.path.exists(full_path) and "Contents/MacOS" in base_path:
        alt_path = os.path.join(os.path.dirname(base_path), "Resources", relative_path)
        if os.path.exists(alt_path):
            return alt_path

    return full_path


class AfplayWrapper:

    def __init__(self, filepath):
        self.filepath = filepath
        self.volume = 1.0
        self.active_processes = []

    def setVolume(self, volume):
        self.volume = volume

    def setLoopCount(self, count):
        pass

    def play(self):
        if self.volume > 0 and os.path.exists(self.filepath):
            self.active_processes = [p for p in self.active_processes if p.poll() is None]

            process = subprocess.Popen(
                ["afplay", "-v", str(self.volume), self.filepath],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.active_processes.append(process)

    def stop(self):
        for p in self.active_processes:
            if p.poll() is None:
                p.terminate()
        self.active_processes = []

    def isPlaying(self):
        self.active_processes = [p for p in self.active_processes if p.poll() is None]
        return len(self.active_processes) > 0


class SoundManager:
    def __init__(self):
        self.sound_paths = {
            "start": "assets/sounds/start.wav",
            "click": "assets/sounds/click.wav",
            "flag": "assets/sounds/flag.wav",
            "flag_remove": "assets/sounds/flag_remove.wav",
            "hint": "assets/sounds/hint.wav",
            "bomb": "assets/sounds/bomb.wav",
            "win": "assets/sounds/win.wav",
            "lose": "assets/sounds/lose.wav",
            "hover": "assets/sounds/hover.wav",
            "error": "assets/sounds/error.wav",
        }

        self.sounds = {name: AfplayWrapper(resource_path(path)) for name, path in self.sound_paths.items()}

    def play(self, name: str):
        if name in self.sounds:
            self.sounds[name].play()

    def stop_all(self):
        for sound in self.sounds.values():
            sound.stop()
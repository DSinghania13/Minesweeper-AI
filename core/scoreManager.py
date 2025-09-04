import json
import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ScoreManager:
    def __init__(self, mode='manual'):
        self.mode = mode.lower()

        if self.mode == 'ai':
            self.filepath = resource_path('json/highscore_ai.json')
        else:
            self.filepath = resource_path('json/highscore_manual.json')

        self.high_score = self.load_high_score()

    def load_high_score(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                try:
                    data = json.load(f)
                    return data.get('high_score', 0)
                except json.JSONDecodeError:
                    return 0
        return 0

    def save_high_score(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, 'w') as f:
            json.dump({'high_score': self.high_score}, f)

    def calculate_score(self, time_taken, hints_used):
        max_time = 999
        hint_penalty = 150

        base_score = max(0, max_time - time_taken)
        final_score = base_score - (hints_used * hint_penalty)

        return max(0, final_score)

    def update_high_score(self, new_score):
        if new_score > self.high_score:
            self.high_score = new_score
            self.save_high_score()
            return True
        return False
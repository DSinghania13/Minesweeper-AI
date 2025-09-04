import sys
import os
import numpy as np
from tensorflow.keras.models import load_model
from ai.rule_based_solver import RuleBasedSolver


def mean_iou(y_true, y_pred): return 0.0


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

MODEL_PATH = resource_path("model/final_rl_model.keras")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Could not find the trained model file at: {MODEL_PATH}")


class AIAgent:
    def __init__(self):
        self.model = load_model(MODEL_PATH, custom_objects={'mean_iou': mean_iou}, compile=False)
        self.solver = RuleBasedSolver()

    def predict_move(self, board_tensor):
        guaranteed_move = self.solver.find_guaranteed_move(board_tensor)
        if guaranteed_move is not None:
            print(f"DEBUG (Solver): Found guaranteed move at ({guaranteed_move[0]}, {guaranteed_move[1]})")
            return guaranteed_move

        print("DEBUG (CNN): No guaranteed move found. Using CNN to predict.")

        input_tensor = np.expand_dims(board_tensor, axis=0)
        q_values = self.model.predict(input_tensor, verbose=0)[0]

        is_hidden = board_tensor[:, :, 0]
        is_flagged = board_tensor[:, :, 1]
        valid_mask_2d = (is_hidden == 1) & (is_flagged == 0)

        valid_mask_flat = np.concatenate([valid_mask_2d.flatten(), valid_mask_2d.flatten()])
        masked_q_values = np.where(valid_mask_flat, q_values, -np.inf)

        best_move_flat_index = np.argmax(masked_q_values)
        row, col, action_type = np.unravel_index(best_move_flat_index, (9, 9, 2))

        return row, col, action_type
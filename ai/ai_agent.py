import sys
import numpy as np
import os
from tensorflow.keras.models import load_model
from ai.rule_based_solver import RuleBasedSolver
from ai.csp_solver import get_probabilities


def mean_iou(y_true, y_pred): return 0.0


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


MODEL_PATH = resource_path("model/best_avg_score_model.keras")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Could not find the trained model file at: {MODEL_PATH}")


class AIAgent:
    def __init__(self):
        self.model = load_model(MODEL_PATH, custom_objects={'mean_iou': mean_iou}, compile=False)
        self.solver = RuleBasedSolver()

    def predict_move(self, board_tensor):
        is_hidden = board_tensor[:, :, 0]
        is_flagged = board_tensor[:, :, 1]
        rows, cols, _ = board_tensor.shape

        # ---------------------------------------------------------
        # 1. Phase 1: Rule-Based Hotspots
        # ---------------------------------------------------------
        guaranteed_move = self.solver.find_guaranteed_move(board_tensor)
        if guaranteed_move is not None:
            print(f"DEBUG (Solver): Found guaranteed move at ({guaranteed_move[0]}, {guaranteed_move[1]})")
            # --- UPDATED: Added "rule_based" tag ---
            return guaranteed_move[0], guaranteed_move[1], guaranteed_move[2], "rule_based_moves"

        # ---------------------------------------------------------
        # 2. Phase 2: Exact CSP Math
        # ---------------------------------------------------------
        print("DEBUG (CSP): No simple rules found. Calculating exact matrix probabilities...")
        csp_board = np.full((rows, cols), -1, dtype=int)

        for r in range(rows):
            for c in range(cols):
                if is_hidden[r, c] == 0 and is_flagged[r, c] == 0:
                    for i in range(9):
                        if board_tensor[r, c, i + 2] == 1:
                            csp_board[r, c] = i
                            break
                elif is_flagged[r, c] == 1:
                    csp_board[r, c] = -2

        csp_probs = get_probabilities(csp_board)

        if csp_probs:
            safe_tiles = [tile for tile, prob in csp_probs.items() if prob == 0.0]
            if safe_tiles:
                print(f"DEBUG (CSP): Found guaranteed safe tile at {safe_tiles[0]}.")
                return safe_tiles[0][0], safe_tiles[0][1], 0, "csp_guarantees"

            mine_tiles = [tile for tile, prob in csp_probs.items() if prob == 1.0]
            if mine_tiles:
                print(f"DEBUG (CSP): Found guaranteed mine at {mine_tiles[0]}.")
                return mine_tiles[0][0], mine_tiles[0][1], 1, "csp_guarantees"

            safest_tile = min(csp_probs, key=csp_probs.get)
            lowest_frontier_prob = csp_probs[safest_tile]

            total_hidden = np.sum(is_hidden == 1)
            total_flagged = np.sum(is_flagged == 1)

            total_cells = rows * cols
            if total_cells >= 480:
                TOTAL_MINES = 99
            elif total_cells >= 256:
                TOTAL_MINES = 40
            else:
                TOTAL_MINES = 10

            remaining_mines = max(0, TOTAL_MINES - total_flagged)

            frontier_tile_count = len(csp_probs)
            dark_tiles = total_hidden - frontier_tile_count

            if dark_tiles > 0:
                global_blind_prob = remaining_mines / dark_tiles
            else:
                global_blind_prob = 1.0

            print(f"DEBUG (CSP): Safest frontier tile is {safest_tile} ({lowest_frontier_prob:.1%} risk).")
            print(f"DEBUG (CSP): Global blind guess risk is {global_blind_prob:.1%}.")

            if lowest_frontier_prob <= global_blind_prob:
                print("DEBUG (CSP): Frontier is safer. Executing local math guess.")
                return safest_tile[0], safest_tile[1], 0, "csp_guesses"
            else:
                print("DEBUG (CSP): The dark is safer! Deferring to CNN for a strategic blind guess.")
                pass

        # ---------------------------------------------------------
        # 3. Phase 3: Deep RL (Blind/Global Guesses)
        # ---------------------------------------------------------
        print("DEBUG (CNN): Using Deep RL to find the most strategic blind spot.")
        input_tensor = np.expand_dims(board_tensor, axis=0)
        q_values = self.model.predict(input_tensor, verbose=0)[0]

        valid_mask_2d = (is_hidden == 1) & (is_flagged == 0)

        if csp_probs:
            for r, c in csp_probs.keys():
                valid_mask_2d[r, c] = False

        disable_flags_mask = np.zeros_like(valid_mask_2d, dtype=bool)

        valid_mask_3d = np.stack([valid_mask_2d, disable_flags_mask], axis=-1)
        valid_mask_flat = valid_mask_3d.flatten()

        valid_indices = np.where(valid_mask_flat)[0]

        if len(valid_indices) == 0:
            print("DEBUG (CNN Fallback): Valid mask empty, taking random safe action.")
            hidden_tiles = np.argwhere((is_hidden == 1) & (is_flagged == 0))
            if len(hidden_tiles) > 0:
                import random
                random_tile = random.choice(hidden_tiles)
                return random_tile[0], random_tile[1], 0, "cnn_guesses"
            else:
                return 0, 0, 0, "cnn_guesses"

        valid_q = q_values[valid_indices]

        best_valid_index = np.argmax(valid_q)
        best_move_flat_index = valid_indices[best_valid_index]
        row, col, action_type = np.unravel_index(best_move_flat_index, board_tensor.shape[:2] + (2,))

        print(f"DEBUG (CNN): Executing strategic blind guess at ({row}, {col}).")
        return row, col, action_type, "cnn_guesses"
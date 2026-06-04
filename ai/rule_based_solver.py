import numpy as np

class RuleBasedSolver:
    def get_neighbors(self, r, c, max_rows, max_cols):
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < max_rows and 0 <= nc < max_cols:
                    neighbors.append((nr, nc))
        return neighbors

    def find_subset_moves(self, board_tensor):
        rows, cols, _ = board_tensor.shape
        is_hidden = board_tensor[:, :, 0]
        is_flagged = board_tensor[:, :, 1]

        number_board = np.zeros((rows, cols), dtype=int)
        for i in range(1, 9):
            number_board[board_tensor[:, :, i + 2] == 1] = i

        constraints = []

        for r in range(rows):
            for c in range(cols):
                if number_board[r, c] > 0 and is_hidden[r, c] == 0:
                    neighbors = self.get_neighbors(r, c, rows, cols)
                    hidden_neighbors = [n for n in neighbors if is_hidden[n] == 1 and is_flagged[n] == 0]
                    flagged_neighbors = [n for n in neighbors if is_flagged[n] == 1]

                    if len(hidden_neighbors) > 0:
                        effective_mines = number_board[r, c] - len(flagged_neighbors)
                        constraints.append({
                            "cells": set(hidden_neighbors),
                            "mines": effective_mines
                        })

        for constraint_A in constraints:
            for constraint_B in constraints:
                if constraint_A == constraint_B:
                    continue

                set_A = constraint_A["cells"]
                set_B = constraint_B["cells"]
                mines_A = constraint_A["mines"]
                mines_B = constraint_B["mines"]

                if set_A.issubset(set_B) and len(set_A) < len(set_B):
                    leftover_cells = set_B - set_A
                    leftover_mines = mines_B - mines_A

                    if leftover_mines == 0:
                        move = leftover_cells.pop()
                        return move[0], move[1], 0

                    elif leftover_mines == len(leftover_cells):
                        move = leftover_cells.pop()
                        return move[0], move[1], 1

        return None

    def find_guaranteed_move(self, board_tensor):
        rows, cols, _ = board_tensor.shape
        is_hidden = board_tensor[:, :, 0]
        is_flagged = board_tensor[:, :, 1]

        number_board = np.zeros((rows, cols), dtype=int)
        for i in range(1, 9):
            number_board[board_tensor[:, :, i + 2] == 1] = i

        for r in range(rows):
            for c in range(cols):
                if number_board[r, c] > 0 and is_hidden[r, c] == 0:
                    neighbors = self.get_neighbors(r, c, rows, cols)
                    flagged_neighbors_count = sum(1 for n in neighbors if is_flagged[n] == 1)
                    if flagged_neighbors_count == number_board[r, c]:
                        hidden_neighbors = [n for n in neighbors if is_hidden[n] == 1 and is_flagged[n] == 0]
                        if hidden_neighbors:
                            safe_r, safe_c = hidden_neighbors[0]
                            return safe_r, safe_c, 0

        for r in range(rows):
            for c in range(cols):
                if number_board[r, c] > 0 and is_hidden[r, c] == 0:
                    neighbors = self.get_neighbors(r, c, rows, cols)
                    flagged_neighbors_count = sum(1 for n in neighbors if is_flagged[n] == 1)
                    hidden_neighbors = [n for n in neighbors if is_hidden[n] == 1 and is_flagged[n] == 0]
                    if len(hidden_neighbors) > 0 and len(hidden_neighbors) == number_board[r, c] - flagged_neighbors_count:
                        bomb_r, bomb_c = hidden_neighbors[0]
                        return bomb_r, bomb_c, 1

        subset_move = self.find_subset_moves(board_tensor)
        if subset_move:
            return subset_move

        return None
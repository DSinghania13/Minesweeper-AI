import numpy as np
import random


class MinesweeperEnv:
    def __init__(self, rows=9, cols=9, bombs=10):
        self.rows = rows
        self.cols = cols
        self.bombs = bombs
        self.action_space_size = rows * cols * 2

    def reset(self):
        self.solution_board = np.zeros((self.rows, self.cols), dtype=int)
        self.visible_board = np.full((self.rows, self.cols), -2, dtype=int)
        self.game_over = False
        self.win = False

        start_row, start_col = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
        self._place_bombs(start_row, start_col)
        self._reveal_tile(start_row, start_col)

        return self._get_state_tensor()

    def step(self, action):
        if self.game_over:
            raise Exception("Cannot take action on a finished game. Please reset the environment.")

        row, col, action_type = np.unravel_index(action, (self.rows, self.cols, 2))

        if action_type == 0:
            if self.visible_board[row, col] >= 0:
                return self._get_state_tensor(), -5, False, {}
            self._reveal_tile(row, col)

        elif action_type == 1:
            self._toggle_flag(row, col)

        reward = self._get_reward()
        self.win = self._check_win()
        if self.win:
            self.game_over = True
            reward = 200

        if self.game_over and not self.win:
            reward = -100

        return self._get_state_tensor(), reward, self.game_over, {}

    def _get_reward(self):
        if self.game_over and not self.win:
            return -100

        return np.sum((self.visible_board >= 0) & (self.solution_board != -1))

    def _place_bombs(self, safe_row, safe_col):
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        positions.remove((safe_row, safe_col))
        bomb_positions = random.sample(positions, self.bombs)

        for r, c in bomb_positions:
            self.solution_board[r, c] = -1

        for r in range(self.rows):
            for c in range(self.cols):
                if self.solution_board[r, c] != -1:
                    self.solution_board[r, c] = self._count_adjacent_bombs(r, c)

    def _count_adjacent_bombs(self, row, col):
        count = 0
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                if self.solution_board[r, c] == -1:
                    count += 1
        return count

    def _reveal_tile(self, row, col):
        if self.visible_board[row, col] != -2:
            return

        if self.solution_board[row, col] == -1:
            self.game_over = True
            self.visible_board[row, col] = -1
            return

        value = self.solution_board[row, col]
        self.visible_board[row, col] = value

        if value == 0:
            self._flood_fill(row, col)

    def _toggle_flag(self, row, col):
        if self.visible_board[row, col] == -2:
            self.visible_board[row, col] = -3
        elif self.visible_board[row, col] == -3:
            self.visible_board[row, col] = -2

    def _flood_fill(self, row, col):
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                if self.visible_board[r, c] == -2:
                    self._reveal_tile(r, c)

    def _check_win(self):
        return np.all((self.visible_board >= 0) | (self.solution_board == -1))

    def _get_state_tensor(self):
        tensor = np.zeros((self.rows, self.cols, 12), dtype=np.float32)
        for r in range(self.rows):
            for c in range(self.cols):
                val = self.visible_board[r, c]
                if val == -2:
                    tensor[r, c, 0] = 1
                elif val == -3:
                    tensor[r, c, 1] = 1
                elif val == 0:
                    tensor[r, c, 2] = 1
                elif val > 0 and val <= 8:
                    tensor[r, c, int(val) + 2] = 1
        return tensor
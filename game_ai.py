import numpy as np
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QAction, QKeySequence
from ai.ai_agent import AIAgent
from game_ui import MinesweeperUI
import random


class AIGameWindow(MinesweeperUI):
    def __init__(self, main_window=None, sound_manager=None):
        super().__init__(mode="ai", main_window=main_window, sound_manager=sound_manager)
        self.setWindowTitle("Minesweeper - AI Mode")
        self.ai_agent = AIAgent()
        self.last_move = None

        self._setup_shortcuts()

        QTimer.singleShot(500, self.start_ai_loop)

    def _setup_shortcuts(self):
        close_action = QAction("Close", self)
        close_action.setShortcuts([QKeySequence("Ctrl+W"), QKeySequence("Meta+W")])
        close_action.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
        close_action.triggered.connect(self.handle_close)
        self.addAction(close_action)

    def handle_close(self):
        print("Handling close via shortcut")
        if hasattr(self, "sounds") and self.sounds:
            self.sounds.stop_all()
        self.game_active = False
        if self.main_window:
            print("Showing main window:", id(self.main_window))
            self.main_window.show()
        self.close()


    def start_ai_loop(self):
        if not self.game_active:
            return

        board_state = self.get_visible_board_state()
        board_tensor = self.convert_to_tensor(board_state)
        print("DEBUG: Calling ai_agent.predict_move...")

        row, col, action_type = self.ai_agent.predict_move(board_tensor)
        print(f"DEBUG: ai_agent.predict_move returned: row={row}, col={col}, action={action_type}")

        current_move = (row, col, action_type)
        if current_move == self.last_move:
            print("DEBUG: AI is repeating a move, forcing a random action.")
            hidden_tiles = np.argwhere((board_tensor[:, :, 0] == 1) & (board_tensor[:, :, 1] == 0))
            if len(hidden_tiles) > 0:
                random_tile = random.choice(hidden_tiles)
                row, col, action_type = random_tile[0], random_tile[1], 0
            else:
                self.check_win()
                return

        self.last_move = (row, col, action_type)
        print(f"DEBUG: AI chose action '{'REVEAL' if action_type == 0 else 'FLAG'}' at ({row}, {col})")

        if action_type == 0:
            self.handle_tile_click(row, col)
        elif action_type == 1:
            self.toggle_flag(row, col)

        if self.game_active:
            QTimer.singleShot(100, self.start_ai_loop)

    def convert_to_tensor(self, visible_board):
        tensor = np.zeros((9, 9, 12), dtype=np.float32)
        for i in range(9):
            for j in range(9):
                val = visible_board[i][j]
                if val == -2:
                    tensor[i][j][0] = 1
                elif val == -3:
                    tensor[i][j][1] = 1
                elif val == 0:
                    tensor[i][j][2] = 1
                elif val > 0 and val <= 8:
                    tensor[i][j][int(val) + 2] = 1
        return tensor

    def reset_game(self):
        super().reset_game()

        self.last_move = None

        QTimer.singleShot(500, self.start_ai_loop)
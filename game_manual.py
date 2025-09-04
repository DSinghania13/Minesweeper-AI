from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import QWidget
from game_ui import MinesweeperUI

class ManualGameWindow(MinesweeperUI):
    def __init__(self, main_window=None, sound_manager=None):
        super().__init__(mode="manual", main_window=main_window, sound_manager=sound_manager)
        self.setWindowTitle("Minesweeper - Manual Mode")
        self._setup_shortcuts()


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

import sys
import json
import os
import time
import random
import datetime
from PyQt6.QtWidgets import (
    QWidget, QPushButton,
    QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QGraphicsOpacityEffect, QMenuBar, QMenu
)
from PyQt6.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QMovie, QAction, QColor, QShortcut, QKeySequence
from core import soundManager
from core.ScoreManager import ScoreManager
from core.hint_manager import HintManager
from core.soundManager import SoundManager
# from devtools.devtools import DevTools


REVEAL_DELAY = 40

DELIMITER = "-" * 50

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join("assets")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Tile:
    def __init__(self, row, col, button, parent):
        self.row = row
        self.col = col
        self.button = button
        self.parent = parent
        self.is_bomb = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_bombs = 0

    def reveal(self, delay=0, callback=None):
        if self.is_revealed or self.is_flagged:
            return

        self.parent.hint_manager.cancel_hint_animation(self)

        def _do_reveal():
            self.is_revealed = True
            self.button.setEnabled(False)

            if self.is_bomb:
                self.button.setText("💣")
                self.button.setStyleSheet("""
                    background-color: #ff4c4c;
                    font-size: 18px;
                    font-weight: bold;
                    color: black;
                    border: 1px solid #5c5c5c;
                    border-radius: 4px;
                """)
            else:
                text = str(self.adjacent_bombs) if self.adjacent_bombs > 0 else ""
                color = {
                    1: "#00BFFF", 2: "#32CD32", 3: "#FF4500",
                    4: "#800080", 5: "#8B0000", 6: "#008B8B",
                    7: "#000000", 8: "#808080"
                }.get(self.adjacent_bombs, "#dddddd")
                self.button.setText(text)
                self.button.setStyleSheet(f"""
                    background-color: #2b2b2b;
                    font-size: 18px;
                    font-weight: bold;
                    color: {color};
                    border: 1px solid #aaaaaa;
                    border-radius: 4px;
                """)

            if callback:
                callback()

        if delay > 0:
            QTimer.singleShot(delay, _do_reveal)
        else:
            _do_reveal()

    def flag(self):
        if self.is_revealed:
            return
        self.is_flagged = not self.is_flagged
        self.button.setText("🚩" if self.is_flagged else "")
        self.parent.hint_manager.cancel_hint_animation(self)


class MinesweeperUI(QWidget):
    def __init__(self, mode="manual", main_window=None, sound_manager=None):
        super().__init__()
        self.main_window = main_window
        if sound_manager:
            self.sounds = sound_manager
        else:
            self.sounds = SoundManager()
        self.sounds.play("start")

        self.mode = mode
        self.setWindowTitle(f"Minesweeper - {'AI' if mode == 'ai' else 'Manual'} Mode")

        self.setFixedSize(440, 480)
        self.setStyleSheet("background-color: #1e1e1e;")
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.tiles = {}

        self.grid_size = 9
        self.num_flags = 10
        self.num_bombs = 10
        self.start_time = None
        self.elapsed_time = 0
        self.timer_started = False
        self.first_click_done = False
        self.game_active = True
        self.board_buttons = {}

        with open(resource_path("json/settings.json"), "r") as f:
            settings = json.load(f)

        self.grid_color = settings.get("grid_color", "#1e90ff")

        self.default_tile_style = """
            QPushButton {
                font-size: 15px;
                color: white;
                background-color: #2b2b2b;
                border: 1px solid #3a3a3a;
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #3a3a3a; }
            QPushButton:pressed { background-color: #1e1e1e; }
        """
        self.safe_hint_style = """
            background-color: #a5d6a7;
            border: 2px solid #388e3c;
            font-weight: bold;
        """
        self.flag_hint_style = """
            background-color: #ef9a9a;
            border: 2px solid #d32f2f;
            font-weight: bold;
        """

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.hint_manager = HintManager(self, self.sounds)
        # Only for developers not for public use
        # self.devtools = DevTools()
        self.score_manager = ScoreManager(mode=self.mode)

        self.init_ui()

    def init_ui(self):
        score_layout = QHBoxLayout()
        score_layout.setSpacing(20)
        top_layout = QHBoxLayout()
        top_layout.setSpacing(20)
        initial_score = self.score_manager.calculate_score(0,0)

        self.current_score_label = QLabel(f"Score: --")
        self.highscore_label = QLabel(f"High Score: {self.score_manager.high_score}")

        self.current_score_label.setStyleSheet("""
                    background-color: #2e2e2e;
                    color: white;
                    padding: 6px 12px;
                    border-radius: 6px;
                    font-size: 15px;
                """)
        self.highscore_label.setStyleSheet("""
                    background-color: #2e2e2e;
                    color: white;
                    padding: 6px 12px;
                    border-radius: 6px;
                    font-size: 15px;
                """)

        score_layout.addStretch(1)
        score_layout.addWidget(self.current_score_label)
        score_layout.addSpacing(50)
        score_layout.addWidget(self.highscore_label)
        score_layout.addStretch(1)

        self.flag_label = QLabel(f"🚩 {self.num_flags}")
        self.flag_label.setStyleSheet("""
            background-color: #2e2e2e;
            color: #FFD700;
            padding: 6px 12px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
        """)
        top_layout.addWidget(self.flag_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.reset_button = QPushButton("😃")
        self.reset_button.setFixedSize(40, 40)
        self.reset_button.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                background-color: #2b2b2b;
                border: 1px solid #3a3a3a;
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #3a3a3a; }
            QPushButton:pressed { background-color: #1e1e1e; }
        """)
        self.reset_button.clicked.connect(self.reset_game)

        self.hint_button = QPushButton("💡 Hint: 5")
        self.hint_button.setFixedSize(120, 40)
        self.hint_button.setStyleSheet("""
            QPushButton {
                font-size: 15px;
                color: white;
                background-color: #2b2b2b;
                border: 1px solid #3a3a3a;
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #3a3a3a; }
            QPushButton:pressed { background-color: #1e1e1e; }
        """)
        self.hint_button.clicked.connect(self.hint_manager.show_hint)

        hover_color = self.adjust_color(self.grid_color, 1.2)
        pressed_color = self.adjust_color(self.grid_color, 0.8)

        unrevealed_style = f"""
            QPushButton {{
                background-color: {self.grid_color};
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                font-size: 18px;
                font-weight: 500;
                color: #dddddd;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                border: 1px solid #4a4a4a;
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
                border: 1px solid #555;
            }}
        """

        reset_hint_layout = QHBoxLayout()
        reset_hint_layout.setSpacing(8)

        reset_hint_layout.addWidget(self.reset_button)
        reset_hint_layout.addWidget(self.hint_button)

        top_layout.addLayout(reset_hint_layout, stretch=0)

        self.time_label = QLabel("⏱️ 0")
        self.time_label.setStyleSheet("""
            background-color: #2e2e2e;
            color: #00BFFF;
            padding: 6px 12px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
        """)
        top_layout.addWidget(self.time_label, alignment=Qt.AlignmentFlag.AlignRight)

        stats_layout = QHBoxLayout()
        stats_layout.setContentsMargins(10, 0, 10, 0)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(4)
        self.buttons = []

        hover_color = self.adjust_color(self.grid_color, 1.2)
        pressed_color = self.adjust_color(self.grid_color, 0.8)

        for row in range(self.grid_size):
            row_tiles = []
            for col in range(self.grid_size):
                btn = QPushButton("")
                btn.setFixedSize(40, 40)
                btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {self.grid_color};
                        border: 1px solid #3a3a3a;
                        border-radius: 4px;
                        font-size: 18px;
                        font-weight: 500;
                        color: #dddddd;
                    }}
                    QPushButton:hover {{
                        background-color: {hover_color};
                        border: 1px solid #4a4a4a;
                    }}
                    QPushButton:pressed {{
                        background-color: {pressed_color};
                        border: 1px solid #555;
                    }}
                """)

                tile = Tile(row, col, btn, self)
                btn.mousePressEvent = lambda event, r=row, c=col: self.handle_mouse_event(event, r, c)

                self.grid_layout.addWidget(btn, row, col)
                row_tiles.append(tile)
            self.buttons.append(row_tiles)

        self.hint_manager.setup(
            hint_button=self.hint_button,
            buttons=self.buttons,
            grid_size=self.grid_size,
            styles={
                "default": self.default_tile_style,
                "safe": self.safe_hint_style,
                "flag": self.flag_hint_style,
                "unrevealed": f"""
                    QPushButton {{
                        background-color: {self.grid_color};
                        border: 1px solid #3a3a3a;
                        border-radius: 4px;
                        font-size: 18px;
                        font-weight: 500;
                        color: #dddddd;
                    }}
                    QPushButton:hover {{
                        background-color: {hover_color};
                        border: 1px solid #4a4a4a;
                    }}
                    QPushButton:pressed {{
                        background-color: {pressed_color};
                        border: 1px solid #555;
                    }}
                """
            }
        )

        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addLayout(score_layout)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(self.grid_layout)
        self.setLayout(main_layout)

        self.explosion_label = QLabel(self)
        self.explosion_label.setFixedSize(100, 100)
        self.explosion_label.setStyleSheet("background: transparent;")
        self.explosion_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.explosion_label.setScaledContents(True)
        self.explosion_movie = QMovie(resource_path("assets/explosion.gif"))
        self.explosion_movie.setCacheMode(QMovie.CacheMode.CacheAll)
        self.explosion_label.setMovie(self.explosion_movie)
        self.explosion_label.hide()

        self.flame_label = QLabel(self)
        self.flame_label.setFixedSize(40, 40)
        self.flame_label.setStyleSheet("background: transparent;")
        self.flame_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.flame_label.setScaledContents(True)
        self.flame_movie = QMovie(resource_path("assets/flame.gif"))
        self.flame_movie.setCacheMode(QMovie.CacheMode.CacheAll)
        self.flame_label.setMovie(self.flame_movie)
        self.flame_label.hide()

        self.game_over_label = self.make_overlay("💥 Game Over")
        self.win_label = self.make_overlay("🎉 You Win!")

        # Only for developers not for public use
        # menu_bar = QMenuBar(self)
        # dev_menu = QMenu("Developer", self)
        #
        # self.dev_action = QAction("Toggle Dev Mode", self)
        # self.dev_action.setCheckable(True)
        # self.dev_action.setChecked(False)
        # self.dev_action.triggered.connect(self.toggle_dev_mode)
        # dev_menu.addAction(self.dev_action)
        #
        # menu_bar.addMenu(dev_menu)
        # main_layout.setMenuBar(menu_bar)

    def adjust_color(self, color_str, factor=1.2):
        color = QColor(color_str)
        r = min(255, int(color.red() * factor))
        g = min(255, int(color.green() * factor))
        b = min(255, int(color.blue() * factor))
        return f"rgb({r}, {g}, {b})"

    def load_settings(self):
        with open(resource_path("json/settings.json"), "r") as f:
            settings = json.load(f)
        self.grid_color = settings.get("grid_color", "#1e90ff")

    def build_grid(self):
        self.load_settings()
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                btn = QPushButton()
                self.apply_button_style(btn)
                self.grid_layout.addWidget(btn, row, col)

    def apply_button_style(self, btn):
        hover_color = self.adjust_color(self.grid_color, 1.2)
        pressed_color = self.adjust_color(self.grid_color, 0.8)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.grid_color};
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                font-size: 18px;
                font-weight: 500;
                color: #dddddd;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
            }}
        """)

    def make_overlay(self, text):
        label = QLabel(text, self)
        label.setStyleSheet("""
            color: white;
            font-size: 26px;
            font-weight: bold;
            background-color: rgba(30, 30, 30, 180);
            border: 2px solid white;
            border-radius: 8px;
            padding: 10px 20px;
        """)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFixedSize(220, 60)
        label.hide()
        return label

    # Only for developers not for public use
    # def toggle_dev_mode(self):
    #     self.devtools.toggle(self)
    #     self.devtools.update_visuals(self)
    #     self.dev_action.setChecked(self.devtools.active)

    def cancel_hint_animation(self, tile):
        if hasattr(tile.button, "_fade_anim"):
            tile.button._fade_anim.stop()
            tile.button.setGraphicsEffect(None)
            del tile.button._fade_anim

        if hasattr(tile, "_original_style_before_hint"):
            tile.button.setStyleSheet(tile._original_style_before_hint)
            del tile._original_style_before_hint

    def get_visible_board_state(self):
        if not hasattr(self, 'buttons') or not self.buttons:
            print("UI Warning: get_visible_board_state called before buttons were initialized.")
            return []

        board_state = []
        for r in range(self.grid_size):
            row_state = []
            for c in range(self.grid_size):
                tile = self.buttons[r][c]

                if tile.is_flagged:
                    row_state.append(-3)
                elif not tile.is_revealed:
                    row_state.append(-2)
                elif tile.is_bomb:
                    row_state.append(-1)
                else:
                    row_state.append(tile.adjacent_bombs)
            board_state.append(row_state)

        return board_state

    def closeEvent(self, event):
        print("Closing MinesweeperUI")
        self.sounds.stop_all()
        if self.main_window:
            print("Showing main window:", id(self.main_window))
            self.main_window.show()
        super().closeEvent(event)


    def handle_mouse_event(self, event, row, col):
        if not self.game_active:
            return
        if event.button() == Qt.MouseButton.LeftButton:
            self.handle_tile_click(row, col)
            self.sounds.play("click")
        elif event.button() == Qt.MouseButton.RightButton:
            self.toggle_flag(row, col)

    def handle_tile_click(self, row, col, is_flagging=False):
        tile = self.buttons[row][col]

        # Only for developers not for public use
        # if self.devtools.active:
        #     action = "bomb" if tile.is_bomb else "reveal"
        #     self.devtools.log_move(row, col, tile, action)

        if tile.is_flagged:
            self.sounds.play("error")
            return

        if not self.timer_started:
            self.start_timer()
            self.timer_started = True

        if not self.first_click_done:
            self.place_bombs(row, col)
            self.first_click_done = True

            # Only for developers not for public use
            # if self.devtools.active:
            #     now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #     print(f"\n🆕 New Game Started at {now} (Dev Mode)\n{DELIMITER}")
            #     self.devtools.start_new_session()
            #     self.devtools.save_metadata("loss")
            #     self.devtools.print_board_snapshot(self.buttons)
            #     self.devtools.export_numpy_snapshot("initial_board", self.buttons)

        # Only for developers not for public use
        # if self.devtools.active:
        #     self.devtools.print_tile_info(row, col, tile, origin=True)

        if tile.is_bomb:
            self.sounds.play("bomb")
            self.timer.stop()
            self.reset_button.setText("😵")
            self.game_active = False
            # Only for developers not for public use
            # if self.devtools.active:
            #     self.devtools.increment_bomb_click()

            btn = tile.button

            center = btn.mapTo(self, btn.rect().center())
            x, y = center.x() - 50, center.y() - 50

            btn.setText("")
            btn.setStyleSheet("""
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 4px;
            """)
            btn.setEnabled(False)

            self.explosion_label.move(x, y)
            self.explosion_label.show()
            self.explosion_movie.start()

            def after_explosion():
                self.explosion_movie.stop()
                self.explosion_label.hide()

                flame_x = btn.mapTo(self, btn.rect().topLeft()).x()
                flame_y = btn.mapTo(self, btn.rect().topLeft()).y()
                self.flame_label.move(flame_x, flame_y)
                self.flame_label.show()
                self.flame_movie.start()

                # Only for developers not for public use
                # if self.devtools.active:
                #     self.devtools.export_numpy_snapshot("bomb_clicked_state", self.buttons)
                self.reveal_all_bombs(exclude=(row, col), clicked_tile=(row, col))
                self.show_game_over()
                # Only for developers not for public use
                # if self.devtools.active:
                #     self.devtools.update_result("loss")
                #     self.devtools.save_metadata("loss")
                #     self.devtools.export_numpy_snapshot("solution_board", self.buttons, reveal_all=True)

            QTimer.singleShot(600, after_explosion)

        elif tile.adjacent_bombs == 0:
            self.flood_reveal(row, col)
        else:
            tile.reveal()

        # Only for developers not for public use
        # if self.devtools.active:
        #     self.devtools.increment_move()

        self.check_win()

    def toggle_flag(self, row, col):
        tile = self.buttons[row][col]
        if tile.is_revealed:
            self.sounds.play("error")
            return
        was_flagged = tile.is_flagged
        tile.flag()
        if tile.is_flagged and not was_flagged:
            self.sounds.play("flag")
            self.num_flags -= 1
        elif not tile.is_flagged and was_flagged:
            self.sounds.play("flag_remove")
            self.num_flags += 1

        self.flag_label.setText(f"🚩 {self.num_flags}")

        # Only for developers not for public use
        # if self.devtools.active:
        #     self.devtools.log_move(row, col, tile, action="flag")
        #     self.devtools.update_flag_count(10 - self.num_flags)

    def flood_reveal(self, row, col):
        stack = [(row, col)]
        visited = set()
        reveal_order = []

        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c))
            tile = self.buttons[r][c]
            if tile.is_revealed or tile.is_flagged:
                continue
            reveal_order.append((r, c))
            if tile.adjacent_bombs == 0:
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                            stack.append((nr, nc))

        for r, c in reveal_order:
            self.buttons[r][c].reveal()

        if reveal_order:
            self.sounds.play("click")

        self.animate_group_pop(reveal_order)

    def animate_group_pop(self, reveal_order):
        if not reveal_order:
            return

        min_row = min(r for r, _ in reveal_order)
        max_row = max(r for r, _ in reveal_order)
        min_col = min(c for _, c in reveal_order)
        max_col = max(c for _, c in reveal_order)

        top_left = self.buttons[min_row][min_col].button.geometry().topLeft()
        bottom_right = self.buttons[max_row][max_col].button.geometry().bottomRight()

        overlay = QLabel(self)
        overlay.setGeometry(top_left.x(), top_left.y(),
                            bottom_right.x() - top_left.x() + 40,
                            bottom_right.y() - top_left.y() + 40)
        overlay.setStyleSheet("background-color: rgba(255, 255, 255, 0.1); border-radius: 10px;")
        overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        overlay.raise_()
        overlay.show()

        shrink = QPropertyAnimation(overlay, b"geometry")
        original = overlay.geometry()
        smaller = original.adjusted(6, 6, -6, -6)
        shrink.setStartValue(original)
        shrink.setEndValue(smaller)
        shrink.setDuration(400)
        shrink.setEasingCurve(QEasingCurve.Type.OutCubic)

        fade = QGraphicsOpacityEffect()
        overlay.setGraphicsEffect(fade)
        fade_anim = QPropertyAnimation(fade, b"opacity")
        fade_anim.setDuration(400)
        fade_anim.setStartValue(0.4)
        fade_anim.setEndValue(0.0)
        fade_anim.setEasingCurve(QEasingCurve.Type.InCubic)
        fade_anim.finished.connect(overlay.deleteLater)

        shrink.start()
        fade_anim.start()

        if not hasattr(self, 'group_pop_animations'):
            self.group_pop_animations = []
        self.group_pop_animations.extend([shrink, fade_anim])

    def reveal_all_bombs(self, exclude=None, clicked_tile=None):
        # Only for developers not for public use
        # if self.devtools.active and clicked_tile:
        #     r, c = clicked_tile
        #     print(f"\nBomb Clicked at [{r},{c}] - Board Before Reveal")
        #     self.devtools.print_board_snapshot(self.buttons, reveal_all=False)
        #     print(DELIMITER)

        self.hint_button.setEnabled(False)
        self.hint_button.setStyleSheet(self.hint_manager.disabled_hint_style)

        for r, row in enumerate(self.buttons):
            for c, tile in enumerate(row):
                if tile.is_bomb and not tile.is_revealed:
                    if exclude and (r, c) == exclude:
                        continue
                    tile.reveal()

    def show_game_over(self):
        self.explosion_movie.stop()
        self.explosion_label.hide()
        self.show_overlay(self.game_over_label)
        self.sounds.play("lose")

        # Only for developers not for public use
        # if self.devtools.active:
        #     print("GAME OVER FINAL SOLUTION:")
        #     self.devtools.print_full_solution(self.buttons)

    def show_win_overlay(self):
        self.show_overlay(self.win_label)
        self.sounds.play("win")
        # Only for developers not for public use
        # if self.devtools.active:
        #     self.devtools.update_result("win")

        # if self.devtools.active:
        #     print("🎉 WIN FINAL SOLUTION:")
        #     self.devtools.export_numpy_snapshot("final_win_state", self.buttons)
        #     self.devtools.print_full_solution(self.buttons)

    def show_overlay(self, label):
        label.move(
            self.width() // 2 - label.width() // 2,
            self.height() // 2 - label.height() // 2
        )
        label.show()

        opacity = QGraphicsOpacityEffect()
        label.setGraphicsEffect(opacity)
        anim = QPropertyAnimation(opacity, b"opacity")
        anim.setDuration(500)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        anim.start()

        self.fade_anim = anim

    def check_win(self):
        for row in self.buttons:
            for tile in row:
                if not tile.is_bomb and not tile.is_revealed:
                    return
        self.timer.stop()
        self.reset_button.setText("😎")
        self.game_active = False

        time_taken = self.elapsed_time
        hints_used = self.hint_manager.hints_used
        new_score = self.score_manager.calculate_score(time_taken, hints_used)

        is_new_highscore = self.score_manager.update_high_score(new_score)
        if is_new_highscore:
            print(f"NEW HIGH SCORE: {new_score}")
            self.highscore_label.setText(f"🏆 {self.score_manager.high_score}")

        self.hint_button.setEnabled(False)
        self.hint_button.setStyleSheet(self.hint_manager.disabled_hint_style)
        self.show_win_overlay()
        # Only for developers not for public use
        # if self.devtools.active:
        #     self.devtools.export_numpy_snapshot("solution_board", self.buttons, reveal_all=True)


    def start_timer(self):
        self.start_time = time.time()
        self.timer.start(1000)

    def update_timer(self):
        if self.start_time:
            self.elapsed_time = int(time.time() - self.start_time)
            self.time_label.setText(f"⏱️ {self.elapsed_time}")

            current_score = self.score_manager.calculate_score(self.elapsed_time, self.hint_manager.hints_used)
            self.current_score_label.setText(f"Score: {current_score}")

    def place_bombs(self, safe_row, safe_col):
        positions = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size)]
        positions.remove((safe_row, safe_col))
        bomb_positions = random.sample(positions, self.num_bombs)

        for r, c in bomb_positions:
            self.buttons[r][c].is_bomb = True

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if not self.buttons[r][c].is_bomb:
                    self.buttons[r][c].adjacent_bombs = self.count_adjacent_bombs(r, c)

        # Only for developers not for public use
        # if self.devtools.active:
        #     self.devtools.update_visuals(self)

    def count_adjacent_bombs(self, row, col):
        return sum(
            self.buttons[r][c].is_bomb
            for r in range(max(0, row - 1), min(self.grid_size, row + 2))
            for c in range(max(0, col - 1), min(self.grid_size, col + 2))
            if (r, c) != (row, col)
        )

    def reset_game(self):
        self.load_settings()
        self.start_time = None
        self.elapsed_time = 0
        self.timer_started = False
        self.first_click_done = False
        self.game_active = True
        self.timer.stop()
        self.num_flags = 10

        self.sounds.stop_all()
        self.time_label.setText("⏱️ 0")
        self.current_score_label.setText("Score: --")
        self.flag_label.setText(f"🚩 {self.num_flags}")
        self.reset_button.setText("😃")
        self.explosion_movie.stop()
        self.explosion_label.hide()
        self.game_over_label.hide()
        self.win_label.hide()
        self.flame_movie.stop()
        self.flame_label.hide()

        for row in self.buttons:
            for tile in row:
                tile.button.setText("")
                tile.button.setEnabled(True)
                self.apply_button_style(tile.button)
                tile.is_bomb = False
                tile.is_revealed = False
                tile.is_flagged = False
                tile.adjacent_bombs = 0

        self.hint_manager.reset()

        # Only for developers not for public use
        # if self.devtools.active:
        #     self.devtools.update_visuals(self)
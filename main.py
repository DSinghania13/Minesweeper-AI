import sys, random
import os
import platform
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel,
    QVBoxLayout, QWidget, QGridLayout, QGraphicsBlurEffect, QGraphicsDropShadowEffect, QMenuBar, QHBoxLayout,
    QRadioButton, QGroupBox, QSlider, QScrollArea
)
from PyQt6.QtGui import QFont, QColor, QAction, QKeySequence
from PyQt6.QtCore import Qt, QEvent
from core.settingsManager import SettingsManager
from core.soundManager import SoundManager
from game_manual import ManualGameWindow
from game_ai import AIGameWindow
from game_ui import MinesweeperUI


if platform.system() == 'Darwin':
    os.environ['QT_MEDIA_BACKEND'] = 'darwin'
if platform.system() == 'Windows':
    os.environ['QT_MEDIA_BACKEND'] = 'windows'
os.environ["QT_LOGGING_RULES"] = "qt.multimedia.ffmpeg.debug=false"


class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")

        self.setWindowTitle("Minesweeper")
        self.setFixedSize(500, 450)
        self.setStyleSheet("background-color: #1e1e1e;")

        self.settings_manager = SettingsManager()
        self.sound_manager = SoundManager()
        self.settings_manager.link_sound_manager(self.sound_manager)

        container = QWidget()
        self.setCentralWidget(container)

        self.unrevealed_bg_tiles = []

        self._create_background_grid(container)
        self._create_main_card(container)
        self._create_settings_card(container)
        self._create_howto_card(container)
        self._create_menu()

    def _create_background_grid(self, container):
        grid_widget = QWidget(container)
        self.grid_widget = grid_widget
        self.grid_layout = QGridLayout(grid_widget)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_widget.setGeometry(0, 0, 500, 450)

        current_color = self.settings_manager.get('grid_color')

        unrevealed_tile_style = f"""
                    background-color: {current_color};
                    border: 1px solid #1e1e1e;
                    border-radius: 0px;
                """
        flag_style = """
                    background-color: #1e1e1e;
                    border: 1px solid #3a3a3a;
                    border-radius: 4px;
                    color: red;
                    font-size: 20px;
                    font-weight: bold;
                """
        number_colors = {
            1: "#00bfff",
            2: "#32cd32",
            3: "#ff4500",
            4: "#8a2be2",
            5: "#ff1493",
            6: "#20b2aa",
            7: "#ffa500",
            8: "#ffffff"
        }

        flag_positions = random.sample(range(120), 6)
        number_positions = random.sample([i for i in range(120) if i not in flag_positions], 10)

        for idx in range(120):
            r, c = divmod(idx, 12)
            if idx in flag_positions:
                tile = QLabel("🚩")
                tile.setAlignment(Qt.AlignmentFlag.AlignCenter)
                tile.setStyleSheet(flag_style)
            elif idx in number_positions:
                num = random.randint(1, 8)
                tile = QLabel(str(num))
                tile.setAlignment(Qt.AlignmentFlag.AlignCenter)
                tile.setStyleSheet(f"""
                                        background-color: #1e1e1e;
                                        border: 1px solid #1e1e1e;
                                        border-radius: 4px;
                                        font-weight: bold;
                                        color: {number_colors[num]};
                                        font-size: 16px;
                                    """)
            else:
                tile = QWidget()
                tile.setObjectName("unrevealedTile")
                tile.setStyleSheet(unrevealed_tile_style)
                self.unrevealed_bg_tiles.append(tile)

            tile.setFixedSize(40, 40)
            self.grid_layout.addWidget(tile, r, c)

        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(12)
        grid_widget.setGraphicsEffect(blur)

    def _create_main_card(self, container):
        self.main_card = QWidget(container)
        self.main_card.setGeometry(50, 50, 400, 350)
        self.main_card.setStyleSheet("""
                        QWidget {
                            background-color: rgba(30, 30, 30, 200);
                            border-radius: 20px;
                        }
                    """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.main_card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.main_card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("💣 Minesweeper")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white; background: transparent;")

        button_style = """
                        QPushButton {
                            font-size: 15px;
                            color: white;
                            background-color: rgba(60, 60, 60, 200);
                            border: none;
                            border-radius: 10px;
                            padding: 12px 24px;
                        }
                        QPushButton:hover {
                            background-color: rgba(90, 90, 90, 220);
                        }
                        QPushButton:pressed {
                            background-color: rgba(40, 40, 40, 230);
                        }
                    """

        self.manual_btn = QPushButton("🎮 Play Manually")
        self.manual_btn.setStyleSheet(button_style)
        self.manual_btn.clicked.connect(self.launch_manual)
        self.manual_btn.installEventFilter(self)

        self.ai_btn = QPushButton("🤖 Watch AI Play")
        self.ai_btn.setStyleSheet(button_style)
        self.ai_btn.clicked.connect(self.launch_ai)
        self.ai_btn.installEventFilter(self)

        card_layout.addWidget(title)
        card_layout.addSpacing(40)
        card_layout.addWidget(self.manual_btn)
        card_layout.addSpacing(15)
        card_layout.addWidget(self.ai_btn)

        utility_layout = QHBoxLayout()
        utility_layout.setContentsMargins(0, 20, 0, 0)
        utility_layout.setSpacing(0)

        utility_button_style = """
                    QPushButton {
                        background-color: rgba(255, 255, 255, 30);
                        border: 1px solid rgba(255, 255, 255, 60);
                        border-radius: 7px;
                        color: white;
                        font-size: 12px;
                        padding: 5px 12px;
                    }
                    QPushButton:hover {
                        background-color: rgba(100, 150, 255, 60);
                    }
                """

        self.howto_btn = QPushButton("❓ How to Play")
        self.howto_btn.setStyleSheet(utility_button_style)
        self.howto_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.howto_btn.clicked.connect(self.open_howto)
        self.howto_btn.installEventFilter(self)

        self.settings_btn = QPushButton("⚙️ Settings")
        self.settings_btn.setStyleSheet(utility_button_style)
        self.settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settings_btn.clicked.connect(self.open_settings)
        self.settings_btn.installEventFilter(self)

        self.quit_btn = QPushButton("🚪 Quit Game")
        self.quit_btn.setStyleSheet(utility_button_style)
        self.quit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.quit_btn.clicked.connect(QApplication.instance().quit)
        self.quit_btn.installEventFilter(self)

        utility_layout.addWidget(self.howto_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        utility_layout.addStretch(1)
        utility_layout.addWidget(self.quit_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        utility_layout.addStretch(1)
        utility_layout.addWidget(self.settings_btn, alignment=Qt.AlignmentFlag.AlignRight)

        card_layout.addStretch(1)
        card_layout.addLayout(utility_layout)

    def _create_settings_card(self, container):
        self.settings_card = QWidget(container)
        self.settings_card.setGeometry(50, 50, 400, 350)
        self.settings_card.setStyleSheet("QWidget { background-color: rgba(30, 30, 30, 200); border-radius: 20px; }")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.settings_card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.settings_card)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Settings")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white; background: transparent; margin-bottom: 20px;")
        layout.addWidget(title)

        volume_section = QVBoxLayout()

        volume_heading = QLabel("Sound Volume")
        volume_heading.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        volume_heading.setAlignment(Qt.AlignmentFlag.AlignLeft)
        volume_section.addWidget(volume_heading)
        volume_section.addSpacing(6)

        volume_layout = QHBoxLayout()
        volume_layout.setContentsMargins(0, 0, 0, 0)
        volume_layout.setSpacing(8)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setFixedHeight(20)
        self.volume_slider.setTracking(True)

        self.volume_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #444;
                height: 6px;
                background: #555;
                border-radius: 3px;
            }
            QSlider::sub-page:horizontal {
                background: #3498db;   /* Blue filled area */
                border: 1px solid #444;
                height: 6px;
                border-radius: 3px;
            }
            QSlider::add-page:horizontal {
                background: #777;  /* Right side (empty) */
                border: 1px solid #444;
                height: 6px;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: white;
                border: 1px solid #444;
                width: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }
        """)
        self.volume_label = QLabel("100%")
        self.volume_label.setStyleSheet("color: white; font-size: 13px; font-weight: bold;")
        self.volume_label.setMinimumWidth(40)
        self.volume_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.volume_slider.valueChanged.connect(lambda v: self.volume_label.setText(f"{v}%"))

        volume_layout.addWidget(self.volume_slider, 1)
        volume_layout.addWidget(self.volume_label, 0)
        volume_section.addLayout(volume_layout)

        volume_section.addSpacing(10)
        layout.addLayout(volume_section)

        color_section = QVBoxLayout()

        color_heading = QLabel("Grid Color")
        color_heading.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        color_heading.setAlignment(Qt.AlignmentFlag.AlignLeft)
        color_section.addWidget(color_heading)
        color_section.addSpacing(6)

        color_layout = QHBoxLayout()
        color_layout.setContentsMargins(0, 0, 0, 0)
        color_layout.setSpacing(12)

        self.color_blue = QRadioButton("Blue")
        self.color_saddle_brown = QRadioButton("Saddle Brown")
        self.color_emerald = QRadioButton("Emerald")
        self.color_orange = QRadioButton("Orange")

        for btn in [self.color_blue, self.color_saddle_brown, self.color_emerald, self.color_orange]:
            btn.setStyleSheet("QRadioButton { color: white; font-size: 13px; }")
            color_layout.addWidget(btn)

        color_layout.addStretch(1)
        color_section.addLayout(color_layout)

        color_section.addSpacing(10)
        layout.addLayout(color_section)

        layout.addStretch(1)

        button_box = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        self.save_btn.setStyleSheet(
            "QPushButton { font-size: 14px; color: white; background-color: #3498db; border-radius: 8px; padding: 8px 16px;}")
        self.cancel_btn.setStyleSheet(
            "QPushButton { font-size: 14px; color: white; background-color: #555; border-radius: 8px; padding: 8px 16px;}")
        button_box.addStretch(1)
        button_box.addWidget(self.cancel_btn)
        button_box.addWidget(self.save_btn)
        layout.addLayout(button_box)

        self.save_btn.installEventFilter(self)
        self.cancel_btn.installEventFilter(self)
        self.save_btn.clicked.connect(self._save_settings)
        self.cancel_btn.clicked.connect(self._close_settings)

        self.settings_card.hide()

    def _create_menu(self):
        menu_bar = QMenuBar(self)
        game_menu = menu_bar.addMenu("Game")
        settings_action = QAction("Settings...", self)
        settings_action.setShortcut(QKeySequence.StandardKey.Preferences)
        settings_action.setMenuRole(QAction.MenuRole.PreferencesRole)
        settings_action.triggered.connect(self.open_settings)
        game_menu.addAction(settings_action)
        self.setMenuBar(menu_bar)

    def open_settings(self):
        self.volume_slider.setValue(self.settings_manager.get('volume'))
        self.volume_label.setText(f"{self.settings_manager.get('volume')}%")

        current_color = self.settings_manager.get('grid_color')
        if current_color == '#998c62':
            self.color_saddle_brown.setChecked(True)
        elif current_color == '#309833':
            self.color_emerald.setChecked(True)
        elif current_color == '#FF8C00':
            self.color_orange.setChecked(True)
        else:
            self.color_blue.setChecked(True)

        self.main_card.hide()
        self.settings_card.show()

    def _save_settings(self):
        self.settings_manager.set('volume', self.volume_slider.value())

        if self.color_saddle_brown.isChecked():
            self.settings_manager.set('grid_color', '#998c62')
        elif self.color_emerald.isChecked():
            self.settings_manager.set('grid_color', '#309833')
        elif self.color_orange.isChecked():
            self.settings_manager.set('grid_color', '#FF8C00')
        else:
            self.settings_manager.set('grid_color', '#0F82F2')


        new_color = self.settings_manager.get('grid_color')
        self._apply_grid_color(new_color)
        self._close_settings()

    def _apply_grid_color(self, new_color: str):
        if not hasattr(self, "grid_layout"):
            return

        for row in range(self.grid_layout.rowCount()):
            for col in range(self.grid_layout.columnCount()):
                item = self.grid_layout.itemAtPosition(row, col)
                if item:
                    widget = item.widget()
                    if widget and widget.objectName() == "unrevealedTile":
                        widget.setStyleSheet(f"""
                            background-color: {new_color};
                            border: 1px solid #1e1e1e;
                        """)

        self.grid_widget.update()
        QApplication.processEvents()

    def _close_settings(self):
        self.settings_card.hide()
        self.main_card.show()

    def _create_howto_card(self, container):
        self.howto_card = QWidget(container)
        self.howto_card.setGeometry(50, 50, 400, 350)
        self.howto_card.setStyleSheet("QWidget { background-color: rgba(30, 30, 30, 200); border-radius: 20px; }")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.howto_card.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.howto_card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        top_bar = QHBoxLayout()
        top_bar.addStretch(1)

        self.howto_close_btn = QPushButton("❌")
        self.howto_close_btn.setFixedSize(28, 28)
        self.howto_close_btn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                color: white;
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                color: #e74c3c;
            }
        """)
        self.howto_close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.howto_close_btn.installEventFilter(self)
        self.howto_close_btn.clicked.connect(self._close_howto)
        top_bar.addWidget(self.howto_close_btn)

        layout.addLayout(top_bar)

        heading = QLabel("How to Play")
        heading.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading.setStyleSheet("color: white; margin-bottom: 10px;")
        layout.addWidget(heading)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        rules_label = QLabel("""
        • The goal is to uncover all tiles without detonating a mine.<br><br>
        • Numbers show how many mines are adjacent.<br><br>
        • Right-click (🚩) to flag suspected mines.<br><br>
        • Use logic to clear safe spaces.<br><br>
        • Win by uncovering all safe tiles!
        """)
        rules_label.setStyleSheet("color: white; font-size: 14px;")
        rules_label.setWordWrap(True)

        content_layout.addWidget(rules_label)
        scroll_area.setWidget(content_widget)

        layout.addWidget(scroll_area)

        self.howto_card.hide()

    def open_howto(self):
        self.main_card.hide()
        self.howto_card.show()

    def _close_howto(self):
        self.howto_card.hide()
        self.main_card.show()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Enter:
            if obj in [
                self.manual_btn,
                self.ai_btn,
                self.howto_btn,
                self.settings_btn,
                self.save_btn,
                self.cancel_btn,
                self.howto_btn,
            ]:
                self.sound_manager.play("hover")

        return super().eventFilter(obj, event)

    def launch_manual(self):
        self.game_window = ManualGameWindow(main_window=self, sound_manager=self.sound_manager)
        self.game_window.show()
        self.hide()

    def launch_ai(self):
        self.game_window = AIGameWindow(main_window=self, sound_manager=self.sound_manager)
        self.game_window.show()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    home = HomePage()
    home.show()
    sys.exit(app.exec())
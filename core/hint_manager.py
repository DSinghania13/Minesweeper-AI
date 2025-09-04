from PyQt6.QtCore import QTimer, QPropertyAnimation, QPoint, Qt
from PyQt6.QtGui import QPainter, QPixmap, QColor, QPolygon
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QLabel, QGraphicsDropShadowEffect

class HintManager:
    def __init__(self, parent_window, sound_manager):
        self.parent = parent_window
        self.sound_manager = sound_manager

        self.default_tile_style = ""
        self.safe_hint_style = ""
        self.flag_hint_style = ""
        self.scheduled_hint_tiles = set()

        self.active_hint_style = """
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

        self.disabled_hint_style = """
            QPushButton {
                background-color: #555;
                color: #ccc;
                border: 1px solid #888;
                border-radius: 6px;
                padding: 4px 12px;
                font-size: 16px;
            }
        """

        self.cooldown_hint_style = """
            QPushButton {
                background-color: #888;
                color: #eee;
                border: 1px solid #aaa;
                border-radius: 6px;
                padding: 4px 12px;
                font-size: 16px;
            }
        """

        self.hint_popup = QLabel("", self.parent)
        self.hint_popup.setStyleSheet("""
            background-color: white;
            border: 2px solid #333;
            border-radius: 8px;
            padding: 6px;
            color: black;
            font-size: 12px;
        """)
        self.hint_popup.setVisible(False)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(2, 2)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.hint_popup.setGraphicsEffect(shadow)

        self.hints_used = 0
        self.hint_limit = 5
        self.buttons = []
        self.hint_button = None
        self.grid_size = 0

        self.hint_triangle = QLabel(self.parent)
        self.hint_triangle.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.hint_triangle.setStyleSheet("background: transparent;")
        self.hint_triangle.setVisible(False)

        self.triangle_down = QPixmap(20, 10)
        self.triangle_down.fill(Qt.GlobalColor.transparent)
        painter = QPainter(self.triangle_down)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor("white"))
        painter.setPen(QColor("#333"))
        points = [QPoint(0, 0), QPoint(20, 0), QPoint(10, 10)]
        painter.drawPolygon(QPolygon(points))
        painter.end()

        self.triangle_up = QPixmap(20, 10)
        self.triangle_up.fill(Qt.GlobalColor.transparent)
        painter = QPainter(self.triangle_up)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor("white"))
        painter.setPen(QColor("#333"))
        points = [QPoint(10, 0), QPoint(0, 10), QPoint(20, 10)]
        painter.drawPolygon(QPolygon(points))
        painter.end()

    def setup(self, hint_button, buttons, grid_size, styles):
        self.hint_button = hint_button
        self.buttons = buttons
        self.grid_size = grid_size
        self.default_tile_style = styles["default"]
        self.safe_hint_style = styles["safe"]
        self.flag_hint_style = styles["flag"]
        self.unrevealed_tile_style = styles["unrevealed"]

    def show_hint(self):
        if self.hints_used >= self.hint_limit:
            self.hint_button.setEnabled(False)
            self.hint_button.setText("💡 No Hints")
            self.hint_button.setStyleSheet(self.disabled_hint_style)
            self.show_hint_exhausted_popup(message="You've used all 5 hints for this game.")
            return None, None

        if not self.hint_button.isEnabled():
            return None, None

        hint_tile, hint_type, reason, src_r, src_c = self.find_best_hint()

        if not hint_tile:
            self.hint_button.setEnabled(False)
            self.hint_button.setStyleSheet(self.cooldown_hint_style)
            self.show_hint_exhausted_popup(
                target=self.hint_button,
                message="No hints right now — try uncovering more tiles.",
                below=True
            )
            QTimer.singleShot(2000, self.restore_hint_button)
            return None, None

        if hint_type == "safe":
            hint_tile.button.setStyleSheet(self.safe_hint_style)
        elif hint_type == "flag":
            hint_tile.button.setStyleSheet(self.flag_hint_style)

        self.sound_manager.play("hint")

        self.show_hint_popup(hint_tile, reason)
        self.highlight_source_tile(src_r, src_c)

        self.hints_used += 1

        # Only for developers not for public use
        # if hasattr(self.parent, "devtools") and self.parent.devtools.active:
        #     board_array = self.parent.devtools.export_board_array(
        #         self.buttons,
        #         include_hint=True,
        #         hint_tile=hint_tile
        #     )
        #     self.parent.devtools.log_hint(
        #         board_array,
        #         hint_tile,
        #         reason=reason,
        #         rule_name="rule-based"
        #     )

        hints_left = self.hint_limit - self.hints_used
        self.hint_button.setText(f"💡 Hint: {hints_left}")
        self.scheduled_hint_tiles.add(hint_tile)
        QTimer.singleShot(2000, lambda: self.fade_out_hint(hint_tile))

        if self.hints_used >= self.hint_limit:
            self.hint_button.setEnabled(False)
            self.hint_button.setText("💡 No Hints")
            self.hint_button.setStyleSheet(self.disabled_hint_style)
            self.show_hint_exhausted_popup()

        return hint_tile, hint_type

    def find_best_hint(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                tile = self.buttons[r][c]
                if not tile.is_revealed or tile.adjacent_bombs == 0:
                    continue

                neighbors = self.get_neighbors(r, c)
                flagged = [t for t in neighbors if t.is_flagged]
                unrevealed = [t for t in neighbors if not t.is_revealed and not t.is_flagged]
                bombs_remaining = tile.adjacent_bombs - len(flagged)

                if bombs_remaining == 0 and len(unrevealed) > 0:
                    return unrevealed[0], "safe", "All bombs already flagged. Safe tiles remain.", r, c

                if bombs_remaining > 0 and bombs_remaining == len(unrevealed):
                    return unrevealed[0], "flag", "Remaining unrevealed tiles must be bombs.", r, c

        return None, None, None, None, None

    def get_neighbors(self, row, col):
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                    neighbors.append(self.buttons[nr][nc])
        return neighbors

    def fade_out_hint(self, tile):
        if tile not in self.scheduled_hint_tiles:
            return
        self.scheduled_hint_tiles.remove(tile)

        anim = getattr(tile.button, "_fade_anim", None)
        if anim:
            anim.stop()
            tile.button.setGraphicsEffect(None)
            tile.button._fade_anim = None

        effect = QGraphicsOpacityEffect()
        tile.button.setGraphicsEffect(effect)

        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(500)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)

        def restore():
            tile.button.setGraphicsEffect(None)
            if not tile.is_revealed:
                tile.button.setStyleSheet(self.unrevealed_tile_style)

        anim.finished.connect(restore)
        anim.start()

        tile.button._fade_anim = anim

    def show_hint_popup(self, target_widget, message, below=False):
        btn = target_widget.button if hasattr(target_widget, "button") else target_widget
        btn_pos = btn.mapToGlobal(btn.rect().topLeft())
        local_pos = self.parent.mapFromGlobal(btn_pos)

        self.hint_popup.setText(message)
        self.hint_popup.adjustSize()

        popup_width = self.hint_popup.width()
        popup_height = self.hint_popup.height()

        max_width = self.parent.width() - popup_width - 10
        popup_x = max(10, min(local_pos.x() + btn.width() // 2 - popup_width // 2, max_width))
        popup_y = local_pos.y() - popup_height - 10 if not below else local_pos.y() + btn.height() + 10

        self.hint_popup.move(popup_x, popup_y)
        self.hint_popup.raise_()
        self.hint_popup.show()

        triangle_pix = self.triangle_down if not below else self.triangle_up
        self.hint_triangle.setPixmap(triangle_pix)

        triangle_width = 20
        triangle_height = 10
        triangle_x = btn.mapTo(self.parent, btn.rect().center()).x() - 10
        triangle_y = popup_y + popup_height - 11 if not below else popup_y - triangle_height

        self.hint_triangle.move(triangle_x, triangle_y)
        self.hint_triangle.raise_()
        self.hint_triangle.show()

        QTimer.singleShot(2500, self.fade_out_hint_popup)

    def show_hint_exhausted_popup(self, target=None, message="No more hints left! (Max 5 per game)", below=True):
        if target is None:
            target = self.hint_button

        btn_pos = target.mapToGlobal(target.rect().topLeft())
        local_pos = self.parent.mapFromGlobal(btn_pos)

        self.hint_popup.setText(message)
        self.hint_popup.adjustSize()

        popup_width = self.hint_popup.width()
        popup_height = self.hint_popup.height()

        max_width = self.parent.width() - popup_width - 10
        popup_x = max(10, min(local_pos.x() + target.width() // 2 - popup_width // 2, max_width))
        popup_y = local_pos.y() + target.height() + 10 if below else local_pos.y() - popup_height - 10

        self.hint_popup.move(popup_x, popup_y)
        self.hint_popup.raise_()
        self.hint_popup.show()

        self.hint_triangle.setPixmap(self.triangle_up if below else self.triangle_down)

        triangle_width = 20
        triangle_height = 18
        triangle_x = target.mapTo(self.parent, target.rect().center()).x() - triangle_width // 2
        triangle_y = popup_y - triangle_height if below else popup_y + popup_height

        self.hint_triangle.move(triangle_x, triangle_y)
        self.hint_triangle.raise_()
        self.hint_triangle.show()

        QTimer.singleShot(2500, self.fade_out_hint_popup)

    def fade_out_hint_popup(self):
        for widget in [self.hint_popup, self.hint_triangle]:
            effect = QGraphicsOpacityEffect()
            widget.setGraphicsEffect(effect)

            anim = QPropertyAnimation(effect, b"opacity")
            anim.setDuration(500)
            anim.setStartValue(1.0)
            anim.setEndValue(0.0)

            def hide_widget(w=widget):
                w.hide()
                w.setGraphicsEffect(None)

            anim.finished.connect(hide_widget)
            anim.start()
            widget._fade_anim = anim

    def restore_hint_button(self):
        if self.hints_used < self.hint_limit:
            self.hint_button.setEnabled(True)
            self.hint_button.setStyleSheet(self.active_hint_style)
            remaining = self.hint_limit - self.hints_used
            self.hint_button.setText(f"💡 Hint: {remaining}")

    def reset(self):
        self.hints_used = 0
        self.hint_button.setEnabled(True)
        self.hint_button.setStyleSheet(self.active_hint_style)
        self.hint_button.setText(f"💡 Hint: {self.hint_limit}")

    def cancel_hint_animation(self, tile):
        self.scheduled_hint_tiles.discard(tile)

        anim = getattr(tile.button, "_fade_anim", None)
        if anim:
            try:
                anim.stop()
                anim.finished.disconnect()
            except Exception:
                pass
            tile.button.setGraphicsEffect(None)
            tile.button._fade_anim = None

        if tile.is_revealed:
            if tile.is_bomb:
                tile.button.setText("💣")
                tile.button.setStyleSheet("""
                    background-color: #ff4c4c;
                    font-size: 18px;
                    font-weight: bold;
                    color: black;
                    border: 1px solid #5c5c5c;
                    border-radius: 4px;
                """)
            else:
                text = str(tile.adjacent_bombs) if tile.adjacent_bombs > 0 else ""
                color = {
                    1: "#00BFFF", 2: "#32CD32", 3: "#FF4500",
                    4: "#800080", 5: "#8B0000", 6: "#008B8B",
                    7: "#000000", 8: "#808080"
                }.get(tile.adjacent_bombs, "#dddddd")
                tile.button.setText(text)
                tile.button.setStyleSheet(f"""
                    background-color: #2b2b2b;
                    font-size: 18px;
                    font-weight: bold;
                    color: {color};
                    border: 1px solid #aaaaaa;
                    border-radius: 4px;
                """)
        else:
            tile.button.setStyleSheet(self.unrevealed_tile_style)
            tile.button.setText("🚩" if tile.is_flagged else "")

    def highlight_source_tile(self, row, col):
        tile = self.buttons[row][col]
        tile.button.setStyleSheet("""
            background-color: #2b2b2b;
            font-size: 18px;
            font-weight: bold;
            color: white;
            border: 2px dashed #FFD700;
            border-radius: 4px;
        """)

        QTimer.singleShot(2000, lambda: self._restore_tile_border(tile))

    def _restore_tile_border(self, tile):
        if tile.is_revealed:
            if tile.is_bomb:
                tile.button.setText("💣")
                tile.button.setStyleSheet("""
                    background-color: #ff4c4c;
                    font-size: 18px;
                    font-weight: bold;
                    color: black;
                    border: 1px solid #5c5c5c;
                    border-radius: 4px;
                """)
            else:
                text = str(tile.adjacent_bombs) if tile.adjacent_bombs > 0 else ""
                color = {
                    1: "#00BFFF", 2: "#32CD32", 3: "#FF4500",
                    4: "#800080", 5: "#8B0000", 6: "#008B8B",
                    7: "#000000", 8: "#808080"
                }.get(tile.adjacent_bombs, "#dddddd")
                tile.button.setText(text)
                tile.button.setStyleSheet(f"""
                    background-color: #2b2b2b;
                    font-size: 18px;
                    font-weight: bold;
                    color: {color};
                    border: 1px solid #aaaaaa;
                    border-radius: 4px;
                """)
        else:
            tile.button.setStyleSheet(self.unrevealed_tile_style)
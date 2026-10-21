"""The Claude bridge's answer: a small panel in the corner, not a paste.

With the bridge on, a spoken command is a question to Claude Code rather than
text for the window in front, so its reply has nowhere to be pasted. It comes up
here instead, beside the indicators, with what was asked above it, a way to copy
it, and a way to carry on in a terminal: the same conversation, opened where
Claude can be watched and can ask before it does something it was not allowed
to do on its own.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
                             QTextBrowser, QVBoxLayout, QWidget)

from . import overlay
from . import theme
from .i18n import t

WIDTH = 440
HEIGHT = 300


class AnswerPanel(QWidget):
    def __init__(self, theme_name=theme.DEFAULT, on_continue=None):
        super().__init__(None)
        self.on_continue = on_continue
        self.corner = "bottom-right"
        self.setWindowTitle("AliDikte")
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        # Up without taking the focus from wherever the typing is; a click on
        # it is still a click.
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setObjectName("home")
        self.resize(WIDTH, HEIGHT)

        layout = QVBoxLayout(self)
        self.question = QLabel("")
        self.question.setObjectName("muted")
        self.question.setWordWrap(True)
        layout.addWidget(self.question)
        self.answer = QTextBrowser()
        self.answer.setOpenExternalLinks(True)
        layout.addWidget(self.answer, 1)
        self.warning = QLabel("")
        self.warning.setWordWrap(True)
        self.warning.hide()
        layout.addWidget(self.warning)

        buttons = QHBoxLayout()
        self.copy_button = QPushButton(t("Copy"))
        self.copy_button.clicked.connect(self.copy)
        self.continue_button = QPushButton(t("Continue in terminal"))
        self.continue_button.setObjectName("primary")
        self.continue_button.clicked.connect(self._continue)
        close = QPushButton(t("Close"))
        close.clicked.connect(self.hide)
        buttons.addWidget(self.copy_button)
        buttons.addStretch(1)
        buttons.addWidget(self.continue_button)
        buttons.addWidget(close)
        layout.addLayout(buttons)
        self.set_theme(theme_name)

    def set_theme(self, name):
        theme.apply(self, name)
        # The shared stylesheet leaves text browsers to the system, which on
        # Windows is a white page under the theme's light text.
        colors = theme.palette(name)
        self.answer.setStyleSheet(
            f"QTextBrowser {{ background: {colors['surface']}; color: {colors['text']};"
            f" border: 1px solid {colors['border']}; border-radius: 8px; padding: 6px; }}")
        self.warning.setStyleSheet(
            "color: #946000;" if name == "light" else "color: #F0B450;")

    def show_answer(self, question, answer, warning="", can_continue=True):
        self.question.setText(question)
        self.answer.setMarkdown(answer)
        self.warning.setText(warning)
        self.warning.setVisible(bool(warning))
        self.continue_button.setVisible(bool(can_continue))
        self._place()
        self.show()
        self.raise_()

    def copy(self):
        QApplication.clipboard().setText(self.answer.toPlainText())

    def _continue(self):
        if self.on_continue is not None:
            self.on_continue()
        self.hide()

    def _place(self):
        area = overlay.active_screen().availableGeometry()
        left = "left" in self.corner
        top = "top" in self.corner
        x = area.left() + overlay.MARGIN if left else area.right() - WIDTH - overlay.MARGIN
        # Clear of the two indicators that share the corner.
        step = 2 * (overlay.HEIGHT + overlay.GAP)
        y = (area.top() + overlay.MARGIN + step if top
             else area.bottom() - HEIGHT - overlay.MARGIN - step)
        self.move(int(x), int(y))

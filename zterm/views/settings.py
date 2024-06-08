from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import *


class Settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.vBoxLayout.setSpacing(20)

        self.title_text = TitleLabel("Z-Term Settings")
        self.hyperlink = HyperlinkLabel(
            QUrl("https://github.com/z-term/zterm.git"), "z-term"
        )

        self.vBoxLayout.addWidget(self.title_text)
        self.vBoxLayout.addWidget(self.hyperlink)

        self.setObjectName("Settings")

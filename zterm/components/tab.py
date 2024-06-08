from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QWidget
from qfluentwidgets import *


class ZTermTab(QFrame):
    def __init__(self, parent, objectName: str, widget: QWidget):
        super().__init__(parent=parent)
        self.widget = widget

        self.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.widget, 0, Qt.AlignCenter)

        self.setObjectName(objectName)

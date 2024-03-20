import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QWidget, QStackedWidget

from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF

from .titlebar import ZTermTitleBar

class TabPage(QFrame):
    """ Tab Page """

    def __init__(self, text: str, objectName, widget: QWidget, icon = None, parent=None):
        super().__init__(parent=parent)
        if icon:
            self.iconWidget = IconWidget(icon, self)
            self.iconWidget.setFixedSize(120, 120)
        self.widget = widget
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.setSpacing(30)
        if icon:
            self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.widget, 0, Qt.AlignCenter)

        self.setObjectName(objectName)

class Terminal(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.vBoxLayout.setSpacing(20)
        
        self.title_text = TitleLabel("Z-Term Terminal Emulator")
        self.load_button = PushButton("/bin/bash")
        self.hyperlink = HyperlinkLabel(QUrl("https://github.com/z-term/zterm.git"), 'z-term')

        self.vBoxLayout.addWidget(self.title_text)
        self.vBoxLayout.addWidget(self.load_button)
        self.vBoxLayout.addWidget(self.hyperlink)

        self.setObjectName("Terminal")

class Settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.vBoxLayout.setSpacing(20)
        
        self.title_text = TitleLabel("Z-Term Settings")
        self.hyperlink = HyperlinkLabel(QUrl("https://github.com/z-term/zterm.git"), 'z-term')

        self.vBoxLayout.addWidget(self.title_text)
        self.vBoxLayout.addWidget(self.hyperlink)

        self.setObjectName("Settings")

class Root(MSFluentWindow):
    def __init__(self):
        super().__init__()

        self.setTitleBar(ZTermTitleBar(self))
        self.tabBar = self.titleBar.tabBar

        self.tabBar.currentChanged.connect(self.onTabChanged)
        self.tabBar.tabAddRequested.connect(self.onTabAddRequested)

        self.init_ui()
        self.init_window()

    def init_ui(self):
        self.stack = QStackedWidget(self, objectName='stack')
        self.addSubInterface(self.stack, FIF.LAYOUT, 'Main_Stack')

        # Hide the unneeded sidebar
        self.navigationInterface.hide()

        self.terminal = Terminal(self)
        self.settings = Settings(self)

        # Tabs
        self.addTab('tab0', 'Powershell', self.terminal, FIF.CODE)
        self.addTab('tab1', 'GitBash', self.terminal, FIF.CODE)
        self.addTab('tab2', 'Settings', self.settings, FIF.SETTING)

    def init_window(self):
        self.resize(1100, 600)
        self.setMinimumWidth(750)
        self.setWindowTitle('Z-Term')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.show()
        QApplication.processEvents()

    def onTabChanged(self, index: int):
        objectName = self.tabBar.currentTab().routeKey()
        self.stack.setCurrentWidget(self.findChild(TabPage, objectName))
        self.stackedWidget.setCurrentWidget(self.stack)

    def onTabAddRequested(self):
        text = f'Powershell <{self.tabBar.count()}>'
        self.addTab(f"tab{self.tabBar.count()}", text, Terminal(self))

    def addTab(self, routeKey, text, widget, icon=None):
        self.tabBar.addTab(routeKey, text, icon)
        self.stack.addWidget(TabPage(text, routeKey, widget, icon, self))
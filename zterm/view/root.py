from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QFrame, QVBoxLayout, QWidget, QStackedWidget

from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF

from .widgets.titlebar import ZTermTitleBar
from .widgets.terminal import Terminal

import uuid

class TabPage(QFrame):
    """ Tab Page """

    def __init__(self, text: str, objectName, widget: QWidget, icon = None, parent=None):
        super().__init__(parent=parent)
        # if icon:
        #     self.iconWidget = IconWidget(icon, self)
        #     self.iconWidget.setFixedSize(120, 120)
        self.widget = widget
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.setSpacing(30)
        # if icon:
        #     self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.widget, 0, Qt.AlignCenter)

        self.setObjectName(objectName)

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
        self.tabBar: TabBar = self.titleBar.tabBar

        self.tabBar.currentChanged.connect(self.onTabChanged)
        self.tabBar.tabAddRequested.connect(self.onTabAddRequested)
        self.tabBar.tabCloseRequested.connect(self.onTabClosed)

        self.init_ui()
        self.init_window()

    def init_ui(self):
        self.stack = QStackedWidget(self, objectName='stack')
        self.addSubInterface(self.stack, FIF.LAYOUT, 'Main_Stack')

        # Hide the unneeded sidebar
        self.navigationInterface.hide()

        # Tabs
        # self.addTab('tab0', 'Terminal', Terminal(self), FIF.CODE)

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
        self.tabBar.setCurrentIndex(index)

    def onTabClosed(self, index: int):
        self.tabBar.setCurrentIndex(index)
        objectName = self.tabBar.currentTab().routeKey()
        tabWidget = self.findChild(TabPage, objectName)
        self.stack.removeWidget(tabWidget)

        self.tabBar.removeTab(index)

    def onTabAddRequested(self):
        text = f'Powershell <{self.tabBar.count()}>'
        self.addTab(f"tab{uuid.uuid4()}", text, Terminal(self))
        self.tabBar.setCurrentIndex(self.tabBar.count() - 1)
        self.onTabChanged(self.tabBar.count() - 1)

    def addTab(self, routeKey, text, widget, icon=None):
        self.tabBar.addTab(routeKey, text, icon)
        self.stack.addWidget(TabPage(text, routeKey, widget, icon, self))
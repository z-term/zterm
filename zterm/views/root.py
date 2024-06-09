import uuid

from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtGui import QResizeEvent
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import *

from zterm.components import *


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
        self.onTabAddRequested()

    def init_ui(self):
        self.stack = QStackedWidget(self, objectName="stack")
        self.stack.setStyleSheet("border: 0;")
        self.addSubInterface(self.stack, FIF.LAYOUT, "Main_Stack")

        # Hide the unneeded sidebar for now
        self.navigationInterface.hide()

    def init_window(self):
        self.resize(700, 400)
        self.setMinimumWidth(700)
        self.setMinimumHeight(400)
        self.setWindowTitle("ZTerm")

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.show()
        QApplication.processEvents()

    def onTabChanged(self, index: int):
        objectName = self.tabBar.currentTab().routeKey()
        self.stack.setCurrentWidget(self.findChild(ZTermTab, objectName))
        self.stackedWidget.setCurrentWidget(self.stack)
        self.tabBar.setCurrentIndex(index)

    def onTabClosed(self, index: int):
        self.tabBar.setCurrentIndex(index)
        objectName = self.tabBar.currentTab().routeKey()
        tabWidget = self.findChild(ZTermTab, objectName)
        self.stack.removeWidget(tabWidget)

        self.tabBar.removeTab(index)

    def onTabAddRequested(self):
        terminal = Terminal(self)
        text = f"{terminal.shell}"
        self.addTab(f"tab{uuid.uuid4()}", text, terminal, FIF.COMMAND_PROMPT)
        self.tabBar.setCurrentIndex(self.tabBar.count() - 1)
        self.onTabChanged(self.tabBar.count() - 1)

    def addTab(self, routeKey, text, widget, icon=None):
        self.tabBar.addTab(routeKey, text, icon)
        self.stack.addWidget(ZTermTab(self, routeKey, widget))
        
    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)

        if (currentTab := self.tabBar.currentTab()) != None:
            objectName = currentTab.routeKey()
            tabWidget = self.findChild(ZTermTab, objectName)
            terminal : Terminal = tabWidget.widget
            terminal.setGeometry(0, 0, event.size().width(), event.size().height())
            terminal.textedit.resize(event.size())
            


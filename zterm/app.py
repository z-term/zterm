from PyQt5.QtCore import QLocale, Qt
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator, Theme, setTheme

from zterm.views import *

QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)


class App(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        setTheme(Theme.DARK)

        self.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
        self.setApplicationName("ZTerm")
        self.setApplicationDisplayName("ZTerm")

        translator = FluentTranslator(QLocale())
        self.installTranslator(translator)

        self.root = Root()
        self.root.show()

    def run(self):
        self.exec_()

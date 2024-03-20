import sys

from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtWidgets import QApplication

from qfluentwidgets import setTheme, Theme, FluentTranslator

from view import Root

QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
app.setApplicationName("ZTerm")
app.setApplicationDisplayName("ZTerm")

# Theme
setTheme(Theme.DARK)

# Translation
translator = FluentTranslator(QLocale())
app.installTranslator(translator)

w = Root()
w.show()

app.exec_()

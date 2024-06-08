import os

from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import *

from zterm.pty import TerminalOutputReader

if os.name == "nt":
    from winpty import PtyProcess as PTY
else:
    from ptyprocess import PtyProcessUnicode as PTY


class Terminal(QWidget):
    """
    A Terminal Widget with all sorts of stuff ongoing
    """

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setObjectName("Terminal")
        self.setContentsMargins(0, 0, 0, 0)

        self.cmd_history = {}
        self.history_level = 0

        self.cwd = os.getcwd()
        self.shell = os.environ.get("COMSPEC") or os.environ.get("SHELL")

        self.process = PTY.spawn([self.shell], cwd=self.cwd)

        self.reader = TerminalOutputReader(self.process)
        self.reader.output_received.connect(self.handle_output)
        self.reader.start()

        self.textedit = PlainTextEdit()
        self.textedit.setStyleSheet(
            """
            background-color: rgba(255, 255, 255, 0.0605);
            border-radius: 0px;
            padding: 5px 5px;
            font-family: 'Cascadia Mono', Consolas, monospace;
            color: white;
            selection-background-color: --ThemeColorPrimary;
            selection-color: black;"""
        )
        self.textedit.setLineWrapMode(PlainTextEdit.LineWrapMode.NoWrap)
        self.textedit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.textedit.setAcceptDrops(True)
        self.textedit.setMinimumSize(parent.width(), parent.height())

        layout = VBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.textedit)

        self.command_end()
        self.textedit.setFocus()
        self.textedit.focusWidget()
        self.textedit.installEventFilter(self)

    def handle_output(self, output):
        self.textedit.insertPlainText(output)
        self.command_end()

    def latest_cmd(self) -> str:
        current_cursor = self.textedit.textCursor()
        start_pos = min(self.input_cursor, current_cursor.position())
        end_pos = max(self.input_cursor, current_cursor.position())

        cursor = QTextCursor(self.textedit.document())
        cursor.setPosition(start_pos)
        cursor.setPosition(end_pos, QTextCursor.KeepAnchor)

        cmd = cursor.selectedText().strip()
        cursor.removeSelectedText()

        self.cmd_history[self.history_level] = cmd
        return cmd

    def run_command(self, cmd: str = ""):
        """Run the command in the terminal"""

        match cmd:
            case "exit":
                quit(cmd[1])
            case "clear":
                self.textedit.setPlainText("")
                self.command_end()
            case _:
                self.cmd_history[self.history_level] = cmd
                self.process.write(cmd + "\r\n")

    def copyText(self):
        self.textedit.copy()

    def pasteText(self):
        self.textedit.paste()

    def setDropEvent(self, event):
        self.textedit.setFocus()
        if event.mimeData().hasUrls():
            f = str(event.mimeData().urls()[0].toLocalFile())
            print("is file:", f)
            if " " in f:
                self.textedit.insertPlainText("'{}'".format(f))
            else:
                self.textedit.insertPlainText(f)
            event.accept()
        elif event.mimeData().hasText():
            ft = event.mimeData().text()
            print("is text:", ft)
            if " " in ft:
                self.textedit.insertPlainText("'{}'".format(ft))
            else:
                self.textedit.insertPlainText(ft)
        else:
            event.ignore()

    def command_end(self):
        """Cleans up the terminal for next command"""

        self.input_cursor = self.textedit.textCursor().position()
        self.textedit.setFocus()

    def closeEvent(self, event):
        """Handle the close event to ensure the reader thread is stopped properly"""

        self.reader.stop()
        self.process.terminate()
        super().closeEvent(event)

    def eventFilter(self, source: QWidget, event: QEvent) -> bool:
        """Event filter for the terminal widget"""

        if source == self.textedit:
            if event.type() == QEvent.DragEnter:
                event.accept()
                return True
            elif event.type() == QEvent.Drop:
                self.setDropEvent(event)
                return True
            elif event.type() == QEvent.KeyPress:
                if event.key() == Qt.Key_Backspace:
                    # if cursor.positionInBlock() <= self.input_pos:
                    #     return True
                    # else:
                    #     return False
                    return False

                elif event.key() == Qt.Key_Return:
                    cmd = self.latest_cmd()
                    self.run_command(cmd)
                    return True

                # elif event.key() == Qt.Key_Left:
                #     if cursor.positionInBlock() <= len(self.prompt):
                #         return True
                #     else:
                #         return False

                # elif event.key() == Qt.Key_Delete:
                #     if cursor.positionInBlock() <= len(self.prompt) - 1:
                #         return True
                #     else:
                #         return False

                # elif (
                #     event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C
                # ):
                #     self.process.kill()
                #     return True

                # elif event.key() == Qt.Key_Up:
                #     try:
                #         if self.track != 0:
                #             cursor.select(QTextCursor.BlockUnderCursor)
                #             cursor.removeSelectedText()
                #             self.textedit.appendPlainText(self.prompt)

                #         self.textedit.insertPlainText(self.cmd_list[self.track])
                #         self.track -= 1

                #     except IndexError:
                #         self.track = 0
                #     return True

                # elif event.key() == Qt.Key_Down:
                #     try:
                #         if self.track != 0:
                #             cursor.select(QTextCursor.BlockUnderCursor)
                #             cursor.removeSelectedText()
                #             self.textedit.appendPlainText(self.prompt)

                #         self.textedit.insertPlainText(self.cmd_list[self.track])
                #         self.track += 1

                #     except IndexError:
                #         self.track = 0
                #     return True

                else:
                    return False
            else:
                return False
        else:
            return False

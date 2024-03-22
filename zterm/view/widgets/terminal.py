from PyQt5.QtCore import Qt, QProcess, QEvent, QStandardPaths
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QWidget

from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF

import sys
import os
import socket
import getpass
import shlex

class Terminal(QWidget):
    """
    A Terminal Widget with all sorts of stuff ongoing
    """
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)

        self.cmd_list = []
        self.track = 0
        os.chdir(os.path.expanduser("~"))
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self.cwd = os.getcwd()

        self.prompt = f"{self.username}@{self.hostname}:{self.cwd}$ "

        self.proc = QProcess(self)
        self.proc.setProcessChannelMode(QProcess.MergedChannels)
        self.proc.readyRead.connect(self.dataReady)
        self.proc.finished.connect(self.isFinished)
        self.proc.setWorkingDirectory(os.getcwd())
        
        self.cmd_window = PlainTextEdit()
        self.cmd_window.setLineWrapMode(PlainTextEdit.NoWrap)
        self.cmd_window.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.cmd_window.setAcceptDrops(True)
        self.cmd_window.setMinimumSize(parent.width(), parent.height())
        self.cursor = self.cmd_window.textCursor()

        layout = VBoxLayout(self)
        layout.addWidget(self.cmd_window)

        self.command_end()
        self.cmd_window.setFocus()
        self.cmd_window.focusWidget()
        self.cmd_window.installEventFilter(self)
        print(self.proc.workingDirectory())

        self.setObjectName("Terminal")

    def latest_cmd(self) -> str:
        """
        This function returns the latest executed command
        """
        return self.cmd_window.toPlainText().strip().split(self.prompt.strip())[-1].replace("'", '"')

    def run_command(self):
        """This function will be called once a command is written and the Enter key is pressed.
        """
        cli = []
        cmd = ""
        t = ""
        cli = shlex.split(self.latest_cmd(), posix=False)
        print(cli)
        cmd = str(cli[0])

        if cmd == "exit":
            quit(cmd[1])

        elif cmd == "clear":
            self.cmd_window.setPlainText("")
            self.command_end()

        elif cmd == "cd":
            del cli[0]
            path = " ".join(cli)
            os.chdir(os.path.abspath(path))
            self.proc.setWorkingDirectory(os.getcwd())
            print("Directory:", self.proc.workingDirectory())
            self.command_end()
        else:
            self.proc.setWorkingDirectory(os.getcwd())
            print("Directory:", self.proc.workingDirectory())
            del cli[0]
            if (QStandardPaths.findExecutable(cmd)):
                self.cmd_list.append(self.latest_cmd())
                print("Command", cmd, "found")
                t = " ".join(cli)
                if self.proc.state() != 2:
                    self.proc.waitForStarted()
                    self.proc.waitForFinished()
                    if "|" in t or ">" in t or "<" in t:
                        print("special characters")
                        self.proc.start('sh -c "' + cmd + ' ' + t + '"')
                        print("running",('sh -c "' + cmd + ' ' + t + '"'))
                    else:
                        self.proc.start(cmd + " " + t)
                        print("running", (cmd + " " + t))
            else:
                print("Command not found ...")
                self.cmd_window.appendPlainText("Command not found ...")
                self.command_end()

    def dataReady(self):
        """
        Called by `self.proc` (`QProcess`) when a running command gives output
        """
        out = ""
        try:
            out = str(self.proc.readAll(), encoding = 'utf8').rstrip()
        except TypeError:
            out = str(self.proc.readAll()).rstrip()
            self.cmd_window.moveCursor(self.cursor.Start)
        self.cmd_window.appendPlainText(out)


    def isFinished(self):
        """
        Called by `self.proc` (`QProcess`) when a running command is finished
        """
        # self.prompt = f"{self.username}@{self.hostname}:{self.cwd}$ "
        # self.cmd_window.appendPlainText(self.prompt)
        self.command_end()

    def eventFilter(self, source, event) -> bool:
        """
        Used to capture and sniff various input events
        """
        if source == self.cmd_window:
            if (event.type() == QEvent.DragEnter):
                event.accept()
                return True
            elif (event.type() == QEvent.Drop):
                self.setDropEvent(event)
                return True
            elif (event.type() == QEvent.KeyPress):
                cursor = self.cmd_window.textCursor()
                if event.key() == Qt.Key_Backspace:
                    if cursor.positionInBlock() <= len(self.prompt):
                        return True
                    else:
                        return False
        
                elif event.key() == Qt.Key_Return:
                    if self.latest_cmd() == "":
                        self.command_end()
                        return True
                    if not self.latest_cmd() == "\\":
                        self.run_command()
                    return True
        
                elif event.key() == Qt.Key_Left:
                    if cursor.positionInBlock() <= len(self.prompt):
                        return True
                    else:
                        return False
            
                elif event.key() == Qt.Key_Delete:
                    if cursor.positionInBlock() <= len(self.prompt) - 1:
                        return True
                    else:
                        return False

                elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
                    self.proc.kill()
                    return True

                elif event.key() == Qt.Key_Up:
                    try:
                        if self.track != 0:
                            cursor.select(QTextCursor.BlockUnderCursor)
                            cursor.removeSelectedText()
                            self.cmd_window.appendPlainText(self.prompt)
        
                        self.cmd_window.insertPlainText(self.cmd_list[self.track])
                        self.track -= 1
        
                    except IndexError:
                        self.track = 0
                    return True

                elif event.key() == Qt.Key_Down:
                    try:
                        if self.track != 0:
                            cursor.select(QTextCursor.BlockUnderCursor)
                            cursor.removeSelectedText()
                            self.cmd_window.appendPlainText(self.prompt)
        
                        self.cmd_window.insertPlainText(self.cmd_list[self.track])
                        self.track += 1
        
                    except IndexError:
                        self.track = 0
                    return True

                else:
                    return False
            else:
                return False
        else:
            return False
        
    def copyText(self):
        self.cmd_window.copy()

    def pasteText(self):
        self.cmd_window.paste()

    def setDropEvent(self, event):
        """
        Handles files drop events
        """
        self.cmd_window.setFocus()
        if event.mimeData().hasUrls():
            f = str(event.mimeData().urls()[0].toLocalFile())
            print("is file:", f)
            if " " in f:
                self.cmd_window.insertPlainText("'{}'".format(f))
            else:
                self.cmd_window.insertPlainText(f)
            event.accept()
        elif event.mimeData().hasText():
            ft = event.mimeData().text()
            print("is text:", ft)
            if " " in ft:
                self.cmd_window.insertPlainText("'{}'".format(ft))
            else:
                self.cmd_window.insertPlainText(ft)
        else:
            event.ignore()

    def command_end(self):
        """
        Cleans up the terminal for next command
        """
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self.cwd = os.getcwd()
        
        self.prompt = f"{self.username}@{self.hostname}:{self.cwd}$ "
        self.cmd_window.appendPlainText(self.prompt)
        cursor = self.cmd_window.textCursor()
        cursor.movePosition(11, 0)
        self.cmd_window.setTextCursor(cursor)
        self.cmd_window.setFocus()
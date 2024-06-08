from __future__ import annotations

import os
import typing

from PyQt5.QtCore import QThread, pyqtSignal

from .ansi import *

if typing.TYPE_CHECKING:
    if os.name == "nt":
        from winpty import PtyProcess as PTY
    else:
        from ptyprocess import PtyProcessUnicode as PTY


class TerminalOutputReader(QThread):
    output_received = pyqtSignal(str)

    def __init__(self, pty):
        super().__init__()
        self.pty = pty
        self.alive = True

    def run(self):
        while self.alive:
            if buf := self.pty.read():
                p = buf.find("\x1b]0;")
                if p != -1:
                    buf = buf[:p]

                buf = "\n".join(
                    [
                        strip_ansi_escape_sequences(i)
                        for i in replace_newline(buf).splitlines()
                    ]
                )

                self.output_received.emit(buf)

    def stop(self):
        self.alive = False
        self.wait()

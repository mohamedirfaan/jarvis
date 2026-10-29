import re
import time
from winpty import PtyProcess
import threading
import queue


class Terminal:
    def __init__(self):
        self.process = PtyProcess.spawn(
            "cmd.exe",
            cwd=r"C:\Code\Jarvis\tools",
        )
        self.output_queue = queue.Queue()
        self.history = []
        self.lock = threading.Lock()

        self.reader = threading.Thread(
            target=self._read_output,
            daemon=True,
        )
        self.reader.start()

    def _read_output(self):
        while self.process.isalive():
            try:
                data = self.process.read(4096)
                if data:
                    self.history.append(data)
                    self.output_queue.put(data)
            except EOFError:
                break
            except Exception as exc:
                self.output_queue.put(
                    f"\n[Terminal reader error: {exc}]"
                )
                break

    def send(self, text: str):
        with self.lock:
            self.process.write(text + "\r")

    def get_recent_output(self) -> str:
        chunks = []

        while True:
            try:
                chunks.append(
                    self.output_queue.get_nowait()
                )
            except queue.Empty:
                break

        return self.clean_output("".join(chunks))

    def clean_output(self, text: str) -> str:
        # Remove common ANSI terminal control sequences.
        text = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", text)

        # Normalize CRLF and standalone CR.
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        return text

    def close(self):
        if self.process.isalive():
            self.process.terminate()


class SystemOperationsTool:
    def __init__(self):
        self.terminals = {1: Terminal()}

    def execute(self, command):
        terminal = self.terminals[1]
        terminal.send(command)
        time.sleep(2)
        return terminal.get_recent_output()

    def getTerminalContent(self):
        terminal = self.terminals[0]
        return terminal.get_recent_output()



import os
import pty
import subprocess

class Terminal:
    def __init__(self):
        self.master, self.slave = pty.openpty()
        self.process = subprocess.Popen(
            ["/bin/sh", "-l"],
            stdin=self.slave,
            stdout=self.slave,
            stderr=self.slave,
            close_fds=True
        )
        os.close(self.slave)
        self.terminal_history = ""

    def execute(self, query):
        endKey = "printf __COMPLETED__\n"
        query += "\n"+endKey
        result = ""
        self.terminal_history += query
        os.write(self.master, query.encode('utf-8'))
        os.read(self.master, len(query.encode('utf-8')))
        while True:
            result += os.read(self.master, 1024).decode('utf-8')
            if "__COMPLETED__" in result:
                break
        self.terminal_history = result
        return self.terminal_history

class SystemOperationsTool:
    def __init__(self):
        self.terminals = {1: Terminal()}

    def execute(self, terminalId, query):
        terminal = self.terminals.get(terminalId)
        if terminal:
            terminal.execute(query)

sys = SystemOperationsTool()
sys.execute(1, "echo \"Hello from py\"")
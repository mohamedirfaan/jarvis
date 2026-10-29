from __future__ import annotations

import os
import subprocess

class Terminal:

    def __init__(self, timeout: float | None = 30.0):
        self.timeout = timeout
        self.terminal_history: list[str] = []

    def execute(self, query: str) -> str:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("Terminal command must be a non-empty string.")
        command = ["cmd.exe", "/d", "/s", "/c", query] if os.name == "nt" else ["/bin/sh", "-lc", query]
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                stdin=subprocess.DEVNULL,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as error:
            output = (error.stdout or "") + (error.stderr or "")
            result = f"{output}\nCommand timed out."
        else:
            result = (completed.stdout + completed.stderr).rstrip("\r\n")
            if completed.returncode != 0:
                result = f"{result}\nCommand exited with code {completed.returncode}.".lstrip("\n")

        self.terminal_history.append(result)
        return result

class SystemOperationsTool:
    def __init__(self):
        self.terminals = {1: Terminal()}

    def execute(self, query: str) -> str:
        try:
            return self.terminals[1].execute(query)
        except Exception as e:
            return f"Error: {e}"
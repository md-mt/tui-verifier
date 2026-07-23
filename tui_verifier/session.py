from __future__ import annotations

import os
import time
from pathlib import Path

import pexpect
import pyte

from .cast import CastRecorder
from .screen import screen_text


KEYS = {
    "enter": "\r",
    "escape": "\x1b",
    "tab": "\t",
    "backspace": "\x7f",
    "up": "\x1b[A",
    "down": "\x1b[B",
    "right": "\x1b[C",
    "left": "\x1b[D",
}


class TerminalSession:
    def __init__(
        self,
        argv: list[str],
        cast_path: Path,
        cwd: str | None,
        env: dict[str, str],
        cols: int,
        rows: int,
    ) -> None:
        self.argv = argv
        self.cast_path = cast_path
        self.cwd = cwd
        self.cols = cols
        self.rows = rows
        self.raw_output = ""
        self.exit_code: int | None = None
        self._screen = pyte.Screen(cols, rows)
        self._stream = pyte.Stream(self._screen)
        merged_env = os.environ.copy()
        if merged_env.get("TERM") in (None, "", "dumb"):
            merged_env["TERM"] = "xterm-256color"
        merged_env.update(env)
        self.recorder = CastRecorder(cast_path, cols, rows, argv)
        self.child: pexpect.spawn | None = None
        self._env = merged_env

    def __enter__(self) -> "TerminalSession":
        self.recorder.__enter__()
        self.child = pexpect.spawn(
            self.argv[0],
            self.argv[1:],
            cwd=self.cwd,
            env=self._env,
            dimensions=(self.rows, self.cols),
            encoding="utf-8",
            codec_errors="replace",
        )
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
        self.recorder.__exit__(*args)

    @property
    def screen(self) -> str:
        return screen_text(self._screen)

    def send_text(self, text: str) -> None:
        self._require_child().send(text)
        self.recorder.input(text)

    def send_line(self, text: str) -> None:
        self.send_text(text + "\r")

    def press(self, key: str) -> None:
        normalized = key.lower()
        if normalized.startswith("ctrl-"):
            self._require_child().sendcontrol(normalized.removeprefix("ctrl-"))
            self.recorder.input(f"<{normalized}>")
            return
        sequence = KEYS[normalized]
        self._require_child().send(sequence)
        self.recorder.input(sequence)

    def wait_for_text(self, text: str, timeout_seconds: float) -> bool:
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            self.read_available(0.05)
            if text in self.screen or text in self.raw_output:
                return True
            if not self.is_alive():
                self.read_available(0)
                return text in self.screen or text in self.raw_output
        return False

    def wait_for_idle(self, stable_seconds: float, timeout_seconds: float) -> bool:
        deadline = time.monotonic() + timeout_seconds
        last_screen = self.screen
        stable_since = time.monotonic()
        while time.monotonic() < deadline:
            self.read_available(0.05)
            current = self.screen
            if current != last_screen:
                last_screen = current
                stable_since = time.monotonic()
            if time.monotonic() - stable_since >= stable_seconds:
                return True
            if not self.is_alive():
                self.read_available(0)
                return True
        return False

    def wait_for_exit(self, timeout_seconds: float) -> int | None:
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            self.read_available(0.05)
            if not self.is_alive():
                return self._collect_exit_code()
        return self.exit_code

    def read_available(self, timeout: float) -> None:
        child = self._require_child()
        if child.closed:
            return
        while True:
            try:
                chunk = child.read_nonblocking(size=4096, timeout=timeout)
            except pexpect.TIMEOUT:
                return
            except pexpect.EOF:
                self._collect_exit_code()
                return
            except ValueError:
                return
            if not chunk:
                return
            self.raw_output += chunk
            self._stream.feed(chunk)
            self.recorder.output(chunk)
            timeout = 0

    def is_alive(self) -> bool:
        child = self._require_child()
        return child.isalive()

    def close(self) -> None:
        if self.child is None:
            return
        try:
            self.read_available(0)
        finally:
            if not self.child.closed and self.child.isalive():
                self.child.close(force=True)
            self._collect_exit_code()

    def _collect_exit_code(self) -> int | None:
        child = self._require_child()
        if self.exit_code is not None:
            return self.exit_code
        if not child.closed:
            child.close()
        if child.exitstatus is not None:
            self.exit_code = int(child.exitstatus)
        elif child.signalstatus is not None:
            self.exit_code = 128 + int(child.signalstatus)
        return self.exit_code

    def _require_child(self) -> pexpect.spawn:
        if self.child is None:
            raise RuntimeError("session has not started")
        return self.child

from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any

from .cast import CastRecorder
from .evidence import new_run_dir, render_artifacts, write_result_files
from .models import AssertionResult, Recipe, RunResult, StepResult, recipe_from_mapping
from .screen import replay_cast
from .session import TerminalSession


def load_recipe(path: Path) -> Recipe:
    return recipe_from_mapping(json.loads(path.read_text(encoding="utf-8")))


class VerificationRunner:
    def run(
        self,
        recipe: Recipe,
        out_dir: Path = Path(".tui-verifier/runs"),
        render_video: bool = False,
    ) -> RunResult:
        start = time.monotonic()
        run_dir = new_run_dir(out_dir, recipe.name)
        run_dir.mkdir(parents=True, exist_ok=True)
        if recipe.command.pty:
            steps, raw_output, exit_code, screen = self._run_pty(recipe, run_dir)
        else:
            steps, raw_output, exit_code, screen = self._run_process(recipe, run_dir)
        artifacts = render_artifacts(run_dir, render_video)
        assertions = self._evaluate_assertions(recipe, screen, raw_output, exit_code)
        passed = all(step.passed for step in steps) and all(a.passed for a in assertions)
        result = RunResult(
            recipe_name=recipe.name,
            passed=passed,
            exit_code=exit_code,
            duration_seconds=time.monotonic() - start,
            steps=steps,
            assertions=assertions,
            artifacts=artifacts,
        )
        write_result_files(run_dir, result)
        return result

    def _run_pty(
        self,
        recipe: Recipe,
        run_dir: Path,
    ) -> tuple[list[StepResult], str, int | None, str]:
        steps: list[StepResult] = []
        with TerminalSession(
            recipe.command.argv,
            run_dir / "session.cast",
            recipe.command.cwd,
            recipe.command.env,
            recipe.cols,
            recipe.rows,
        ) as session:
            for index, step in enumerate(recipe.steps, start=1):
                step_result = self._run_step(session, index, step)
                steps.append(step_result)
                if not step_result.passed:
                    break
            if recipe.expect_exit_code is not None:
                session.wait_for_exit(recipe.timeout_seconds)
            else:
                session.wait_for_idle(0.5, min(3, recipe.timeout_seconds))
            return steps, session.raw_output, session.exit_code, session.screen

    def _run_process(
        self,
        recipe: Recipe,
        run_dir: Path,
    ) -> tuple[list[StepResult], str, int | None, str]:
        env = os.environ.copy()
        if env.get("TERM") in (None, "", "dumb"):
            env["TERM"] = "xterm-256color"
        env.update(recipe.command.env)
        cast_path = run_dir / "session.cast"
        with CastRecorder(cast_path, recipe.cols, recipe.rows, recipe.command.argv) as recorder:
            try:
                completed = subprocess.run(
                    recipe.command.argv,
                    cwd=recipe.command.cwd,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    timeout=recipe.timeout_seconds,
                )
                raw_output = completed.stdout
                exit_code: int | None = completed.returncode
            except subprocess.TimeoutExpired as error:
                raw_output = _timeout_output(error)
                exit_code = None
            recorder.output(raw_output)
        screen, _, _ = replay_cast(cast_path)
        steps = self._evaluate_output_steps(recipe, screen, raw_output)
        return steps, raw_output, exit_code, screen

    def _run_step(
        self,
        session: TerminalSession,
        index: int,
        step: dict[str, Any],
    ) -> StepResult:
        action = step["action"]
        name = step.get("name", f"{index}:{action}")
        if action == "wait_for_text":
            text = step["text"]
            timeout = float(step.get("timeout_seconds", 10))
            passed = session.wait_for_text(text, timeout)
            detail = f"found {text!r}" if passed else f"timed out waiting for {text!r}"
            return StepResult(name, passed, detail, session.screen)
        if action == "wait_for_idle":
            stable = float(step.get("stable_seconds", 0.5))
            timeout = float(step.get("timeout_seconds", 10))
            passed = session.wait_for_idle(stable, timeout)
            detail = f"stable for {stable}s" if passed else "timed out waiting for idle"
            return StepResult(name, passed, detail, session.screen)
        if action == "send_text":
            session.send_text(step["text"])
            return StepResult(name, True, "sent text", session.screen)
        if action == "send_line":
            session.send_line(step.get("text", ""))
            return StepResult(name, True, "sent line", session.screen)
        if action == "press":
            session.press(step["key"])
            return StepResult(name, True, f"pressed {step['key']}", session.screen)
        if action == "sleep":
            time.sleep(float(step.get("seconds", 1)))
            session.read_available(0)
            return StepResult(name, True, "slept", session.screen)
        raise ValueError(f"unknown step action: {action}")

    def _evaluate_output_steps(
        self,
        recipe: Recipe,
        screen: str,
        raw_output: str,
    ) -> list[StepResult]:
        results: list[StepResult] = []
        for index, step in enumerate(recipe.steps, start=1):
            action = step["action"]
            name = step.get("name", f"{index}:{action}")
            if action == "wait_for_text":
                text = step["text"]
                passed = text in screen or text in raw_output
                detail = f"found {text!r}" if passed else f"missing {text!r}"
                results.append(StepResult(name, passed, detail, screen))
            elif action == "sleep":
                results.append(StepResult(name, True, "not needed for process mode", screen))
            else:
                detail = f"{action!r} requires command.pty=true"
                results.append(StepResult(name, False, detail, screen))
        return results

    def _evaluate_assertions(
        self,
        recipe: Recipe,
        screen: str,
        raw_output: str,
        exit_code: int | None,
    ) -> list[AssertionResult]:
        assertions = list(recipe.assertions)
        if recipe.expect_exit_code is not None:
            assertions.append({"type": "exit_code", "value": recipe.expect_exit_code})
        return [
            self._evaluate_assertion(recipe, assertion, screen, raw_output, exit_code)
            for assertion in assertions
        ]

    def _evaluate_assertion(
        self,
        recipe: Recipe,
        assertion: dict[str, Any],
        screen: str,
        raw_output: str,
        exit_code: int | None,
    ) -> AssertionResult:
        kind = assertion["type"]
        value = assertion.get("value")
        name = assertion.get("name", kind)
        if kind == "output_contains":
            return _contains(name, raw_output, value, True)
        if kind == "output_not_contains":
            return _contains(name, raw_output, value, False)
        if kind == "screen_contains":
            return _contains(name, screen, value, True)
        if kind == "screen_not_contains":
            return _contains(name, screen, value, False)
        if kind == "exit_code":
            passed = exit_code == value
            return AssertionResult(name, passed, f"expected {value}, got {exit_code}")
        if kind == "file_exists":
            path = _recipe_path(recipe, str(value))
            return AssertionResult(name, path.exists(), str(path))
        if kind == "file_contains":
            path = _recipe_path(recipe, str(assertion["path"]))
            text = path.read_text(encoding="utf-8") if path.exists() else ""
            return _contains(name, text, value, True)
        raise ValueError(f"unknown assertion type: {kind}")


def _contains(name: str, haystack: str, needle: str, should_contain: bool) -> AssertionResult:
    found = needle in haystack
    passed = found if should_contain else not found
    expectation = "contains" if should_contain else "does not contain"
    return AssertionResult(name, passed, f"{expectation} {needle!r}")


def _recipe_path(recipe: Recipe, path: str) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    base = Path(recipe.command.cwd or ".")
    return base / candidate


def _timeout_output(error: subprocess.TimeoutExpired) -> str:
    stdout = error.stdout or ""
    stderr = error.stderr or ""
    if isinstance(stdout, bytes):
        stdout = stdout.decode(errors="replace")
    if isinstance(stderr, bytes):
        stderr = stderr.decode(errors="replace")
    return f"{stdout}{stderr}\n[TUI Verifier timed out]"

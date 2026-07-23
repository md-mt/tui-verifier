from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from .models import RunResult
from .screen import render_svg, replay_cast


def new_run_dir(base_dir: Path, recipe_name: str) -> Path:
    safe_name = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in recipe_name)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return base_dir / f"{timestamp}-{safe_name}"


def render_artifacts(run_dir: Path, render_video: bool) -> dict[str, str]:
    cast_path = run_dir / "session.cast"
    final_text, cols, rows = replay_cast(cast_path)
    final_txt = run_dir / "final.txt"
    final_svg = run_dir / "final.svg"
    final_txt.write_text(final_text + "\n", encoding="utf-8")
    render_svg(final_text, final_svg, cols, rows)
    artifacts = {
        "cast": str(cast_path),
        "screenshot": str(final_svg),
        "screen_text": str(final_txt),
    }
    if render_video and shutil.which("agg"):
        gif_path = run_dir / "session.gif"
        subprocess.run(["agg", "--quiet", str(cast_path), str(gif_path)], check=True)
        artifacts["video"] = str(gif_path)
    return artifacts


def write_result_files(run_dir: Path, result: RunResult) -> None:
    (run_dir / "result.json").write_text(
        json.dumps(result.to_dict(), indent=2) + "\n",
        encoding="utf-8",
    )
    (run_dir / "report.md").write_text(render_report(result), encoding="utf-8")


def render_report(result: RunResult) -> str:
    verdict = "PASS" if result.passed else "FAIL"
    lines = [
        f"# TUI Verification - {verdict}",
        "",
        f"- Recipe: `{result.recipe_name}`",
        f"- Exit code: `{result.exit_code}`",
        f"- Duration: `{result.duration_seconds:.2f}s`",
        "",
        "## Artifacts",
        "",
    ]
    for name, path in result.artifacts.items():
        lines.append(f"- {name}: `{path}`")
    lines.extend(["", "## Assertions", ""])
    for assertion in result.assertions:
        mark = "PASS" if assertion.passed else "FAIL"
        lines.append(f"- {mark} `{assertion.name}` - {assertion.detail}")
    lines.extend(["", "## Steps", ""])
    for step in result.steps:
        mark = "PASS" if step.passed else "FAIL"
        lines.append(f"- {mark} `{step.name}` - {step.detail}")
    return "\n".join(lines) + "\n"

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CommandSpec:
    argv: list[str]
    cwd: str | None = None
    env: dict[str, str] = field(default_factory=dict)
    pty: bool = True


@dataclass(frozen=True)
class Recipe:
    name: str
    command: CommandSpec
    description: str = ""
    steps: list[dict[str, Any]] = field(default_factory=list)
    assertions: list[dict[str, Any]] = field(default_factory=list)
    expect_exit_code: int | None = 0
    timeout_seconds: float = 30.0
    cols: int = 100
    rows: int = 30


@dataclass(frozen=True)
class StepResult:
    name: str
    passed: bool
    detail: str
    screen: str


@dataclass(frozen=True)
class AssertionResult:
    name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class RunResult:
    recipe_name: str
    passed: bool
    exit_code: int | None
    duration_seconds: float
    steps: list[StepResult]
    assertions: list[AssertionResult]
    artifacts: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "recipe_name": self.recipe_name,
            "passed": self.passed,
            "exit_code": self.exit_code,
            "duration_seconds": self.duration_seconds,
            "steps": [step.__dict__ for step in self.steps],
            "assertions": [assertion.__dict__ for assertion in self.assertions],
            "artifacts": self.artifacts,
        }


def recipe_from_mapping(data: dict[str, Any]) -> Recipe:
    command_data = data["command"]
    command = CommandSpec(
        argv=list(command_data["argv"]),
        cwd=command_data.get("cwd"),
        env=dict(command_data.get("env", {})),
        pty=bool(command_data.get("pty", True)),
    )
    return Recipe(
        name=data["name"],
        description=data.get("description", ""),
        command=command,
        steps=list(data.get("steps", [])),
        assertions=list(data.get("assertions", [])),
        expect_exit_code=data.get("expect_exit_code", 0),
        timeout_seconds=float(data.get("timeout_seconds", 30)),
        cols=int(data.get("cols", 100)),
        rows=int(data.get("rows", 30)),
    )

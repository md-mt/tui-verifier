# TUI Verifier

TUI Verifier is an evidence-first verification harness for terminal and TUI
applications. It launches a target command in a PTY, drives it with recipe
steps, records an asciinema v2 cast, derives a terminal screenshot from the
cast, optionally renders a 60-fps MP4 video with `agg` plus `ffmpeg`, and
writes a compact report.

The initial showcase recipes target the Pi coding agent because Pi is a real
terminal coding assistant with a stable local CLI surface.

## Quickstart

```bash
uv run tui-verify run examples/pi_help.recipe.json --video
uv run tui-verify run examples/pi_version.recipe.json --video
uv run tui-verify run examples/pi_list.recipe.json --video
uv run tui-verify run examples --priority P0 --renderer all --video
uv run tui-verify list examples --priority P0
```

Each run writes artifacts under `.tui-verifier/runs/<run-id>/`:

- `session.cast` - asciinema v2 terminal recording
- `final.svg` - final terminal screenshot derived by replaying the cast
- `final.txt` - final terminal screen text
- `session.mp4` - 60-fps H.264 video rendered with `agg` plus `ffmpeg`
- `result.json` - machine-readable verdict and artifact paths
- `report.md` - review-friendly summary
- `latest-report.md` - aggregate report when multiple recipes/renderers run

Tracked Pi sample artifacts are included under `examples/artifacts/`.

## Stack Design

The harness follows the same architecture as the MetaCode TUI validation stack:

- recipe metadata: `priority`, `execution`, `determinism`, `checks`, `ci_paths`
- recipe discovery and selection from `*.recipe.json` files
- renderer expansion with `--renderer default|all|<name>`
- per-run build provenance in aggregate reports
- evidence-first artifacts: cast, screenshot, MP4 video, result JSON, report
- before/after delta primitives for guardrail-style comparisons

## Recipe Format

Recipes are JSON files so they can live beside any project without importing
Python code.

```json
{
  "name": "hello-terminal",
  "priority": "P0",
  "execution": "scripted",
  "determinism": "deterministic",
  "checks": ["terminal prints hello"],
  "renderers": { "default": [] },
  "command": { "argv": ["python3", "-c", "print('hello tui')"], "pty": true },
  "steps": [
    { "action": "wait_for_text", "text": "hello tui", "timeout_seconds": 5 }
  ],
  "assertions": [
    { "type": "output_contains", "value": "hello tui" }
  ],
  "expect_exit_code": 0
}
```

Supported step actions:

- `wait_for_text`
- `wait_for_idle`
- `send_text`
- `send_line`
- `press`
- `sleep`

Supported assertions:

- `output_contains`
- `output_not_contains`
- `screen_contains`
- `screen_not_contains`
- `exit_code`
- `file_exists`
- `file_contains`

`command.pty` defaults to `true` for interactive TUI coverage. Set it to
`false` for terminal commands that should be captured without an interactive
PTY, while still producing asciinema-derived evidence.

`renderers` maps renderer names to extra argv appended to the command. For a
TUI with two frontends, a recipe can declare `{"opentui": [], "ink": ["-x",
"ink"]}` and `--renderer all` will run both.

The Pi examples do not assert a fixed exit code because Meta launcher sandbox
policy differs by machine. The actual exit code is still recorded in
`result.json` and `report.md`.

## Why Asciinema First

The cast is the source of truth. Screenshots and videos are generated from the
same terminal recording that the verifier used for assertions, so reviewers can
inspect what happened instead of trusting a private terminal session.

This mirrors the product-validation direction from the MetaCode TUI validation
docs: drive the real terminal surface, assert product outcomes, and publish
reviewable evidence.

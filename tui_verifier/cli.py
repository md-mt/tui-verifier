from __future__ import annotations

import argparse
from pathlib import Path

from .runner import VerificationRunner, load_recipe


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="tui-verify")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run", help="run a verification recipe")
    run_parser.add_argument("recipe", type=Path)
    run_parser.add_argument("--out", type=Path, default=Path(".tui-verifier/runs"))
    run_parser.add_argument("--video", action="store_true")
    run_parser.add_argument("--no-video", action="store_true")
    run_parser.add_argument("--video-fps", type=int, default=60)
    args = parser.parse_args(argv)

    if args.command == "run":
        recipe = load_recipe(args.recipe)
        result = VerificationRunner().run(
            recipe,
            out_dir=args.out,
            render_video=args.video and not args.no_video,
            video_fps=args.video_fps,
        )
        verdict = "PASS" if result.passed else "FAIL"
        print(f"{verdict} {result.recipe_name}")
        print(f"report: {result.artifacts['cast'].removesuffix('session.cast')}report.md")
        if "video" in result.artifacts:
            print(f"video: {result.artifacts['video']}")
        print(f"screenshot: {result.artifacts['screenshot']}")
        return 0 if result.passed else 1
    return 2

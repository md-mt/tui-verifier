# TUI Verification - PASS

- Recipe: `pi-list`
- Renderer: `default`
- Priority: `P0`
- Execution: `scripted`
- Score: `1.00`
- Exit code: `71`
- Duration: `1.96s`

## Artifacts

- cast: `examples/artifacts/20260724-004054-385805-pi-list-default/session.cast`
- screenshot: `examples/artifacts/20260724-004054-385805-pi-list-default/final.svg`
- screen_text: `examples/artifacts/20260724-004054-385805-pi-list-default/final.txt`
- step_screenshots: `examples/artifacts/20260724-004054-385805-pi-list-default/steps`
- video: `examples/artifacts/20260724-004054-385805-pi-list-default/session.mp4`

## Assertions

- PASS `output_contains` - contains 'Pi at Meta'
- PASS `output_contains` - contains 'Using AI Gateway'

## Steps

- PASS `1:wait_for_text` - found 'Pi at Meta'

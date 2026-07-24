# TUI Verification - PASS

- Recipe: `pi-version`
- Renderer: `default`
- Priority: `P0`
- Execution: `scripted`
- Score: `1.00`
- Exit code: `71`
- Duration: `1.93s`

## Artifacts

- cast: `examples/artifacts/20260724-004056-344321-pi-version-default/session.cast`
- screenshot: `examples/artifacts/20260724-004056-344321-pi-version-default/final.svg`
- screen_text: `examples/artifacts/20260724-004056-344321-pi-version-default/final.txt`
- step_screenshots: `examples/artifacts/20260724-004056-344321-pi-version-default/steps`
- video: `examples/artifacts/20260724-004056-344321-pi-version-default/session.mp4`

## Assertions

- PASS `output_contains` - contains 'Pi at Meta'
- PASS `output_contains` - contains 'Using AI Gateway'

## Steps

- PASS `1:wait_for_text` - found 'Pi at Meta'

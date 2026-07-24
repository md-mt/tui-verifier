# TUI Verification - PASS

- Recipe: `pi-help`
- Renderer: `default`
- Priority: `P0`
- Execution: `scripted`
- Score: `1.00`
- Exit code: `71`
- Duration: `3.21s`

## Artifacts

- cast: `examples/artifacts/20260724-004051-177323-pi-help-default/session.cast`
- screenshot: `examples/artifacts/20260724-004051-177323-pi-help-default/final.svg`
- screen_text: `examples/artifacts/20260724-004051-177323-pi-help-default/final.txt`
- step_screenshots: `examples/artifacts/20260724-004051-177323-pi-help-default/steps`
- video: `examples/artifacts/20260724-004051-177323-pi-help-default/session.mp4`

## Assertions

- PASS `output_contains` - contains 'Pi at Meta'
- PASS `output_contains` - contains 'Meta Launcher Options'
- PASS `output_contains` - contains '--doctor'

## Steps

- PASS `1:wait_for_text` - found 'Meta Launcher Options'

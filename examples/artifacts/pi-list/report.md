# TUI Verification - PASS

- Recipe: `pi-list`
- Renderer: `default`
- Priority: `P0`
- Execution: `scripted`
- Score: `1.00`
- Exit code: `71`
- Duration: `1.87s`

## Artifacts

- cast: `examples/artifacts/pi-list/session.cast`
- screenshot: `examples/artifacts/pi-list/final.svg`
- screen_text: `examples/artifacts/pi-list/final.txt`
- video: `examples/artifacts/pi-list/session.mp4`

## Assertions

- PASS `output_contains` - contains 'Pi at Meta'
- PASS `output_contains` - contains 'Using AI Gateway'

## Steps

- PASS `1:wait_for_text` - found 'Pi at Meta'

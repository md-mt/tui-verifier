# TUI Verification - PASS

- Recipe: `pi-help`
- Exit code: `71`
- Duration: `4.86s`

## Artifacts

- cast: `.tui-verifier/runs/20260723-152144-pi-help/session.cast`
- screenshot: `.tui-verifier/runs/20260723-152144-pi-help/final.svg`
- screen_text: `.tui-verifier/runs/20260723-152144-pi-help/final.txt`
- video: `.tui-verifier/runs/20260723-152144-pi-help/session.mp4`

## Assertions

- PASS `output_contains` - contains 'Pi at Meta'
- PASS `output_contains` - contains 'Meta Launcher Options'
- PASS `output_contains` - contains '--doctor'

## Steps

- PASS `1:wait_for_text` - found 'Meta Launcher Options'

# TUI Verification - 3/3 Passed

## Build Provenance

- Mode: `installed`
- Command: `pi --help`
- Binary: `/usr/local/bin/pi`
- Version: `Pi at Meta (https://www.npmjs.com/package/@earendil-works/pi-coding-agent) / Using AI Gateway (Anthropic upstream) / sandbox-exec: sandbox_apply: Operation not permitted`
- Git commit: `a5789af12b90027607e61b62120f72de2938bed9`
- Verified: `yes`

| Recipe | Renderer | Priority | Execution | Result | Score | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `pi-help` | `default` | `P0` | `scripted` | PASS | 1.00 | [screenshot](pi-help/final.svg) / [video](pi-help/session.mp4) / [cast](pi-help/session.cast) / [screen_text](pi-help/final.txt) |
| `pi-list` | `default` | `P0` | `scripted` | PASS | 1.00 | [screenshot](pi-list/final.svg) / [video](pi-list/session.mp4) / [cast](pi-list/session.cast) / [screen_text](pi-list/final.txt) |
| `pi-version` | `default` | `P0` | `scripted` | PASS | 1.00 | [screenshot](pi-version/final.svg) / [video](pi-version/session.mp4) / [cast](pi-version/session.cast) / [screen_text](pi-version/final.txt) |

<details><summary>PASS pi-help [default]</summary>

### Assertions

- PASS `output_contains` - contains 'Pi at Meta'
- PASS `output_contains` - contains 'Meta Launcher Options'
- PASS `output_contains` - contains '--doctor'

### Steps

- PASS `1:wait_for_text` - found 'Meta Launcher Options'

</details>

<details><summary>PASS pi-list [default]</summary>

### Assertions

- PASS `output_contains` - contains 'Pi at Meta'
- PASS `output_contains` - contains 'Using AI Gateway'

### Steps

- PASS `1:wait_for_text` - found 'Pi at Meta'

</details>

<details><summary>PASS pi-version [default]</summary>

### Assertions

- PASS `output_contains` - contains 'Pi at Meta'
- PASS `output_contains` - contains 'Using AI Gateway'

### Steps

- PASS `1:wait_for_text` - found 'Pi at Meta'

</details>

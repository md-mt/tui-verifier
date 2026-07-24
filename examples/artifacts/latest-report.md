# TUI Verification - 3/3 Passed

## Build Provenance

- Mode: `installed`
- Command: `pi --help`
- Binary: `/usr/local/bin/pi`
- Version: `Pi at Meta (https://www.npmjs.com/package/@earendil-works/pi-coding-agent) / Using AI Gateway (Anthropic upstream) / sandbox-exec: sandbox_apply: Operation not permitted`
- Git commit: `4d696ee013d37d06084e2e26b09ac09bbb1710bf`
- Verified: `yes`

| Recipe | Renderer | Priority | Execution | Result | Score | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `pi-help` | `default` | `P0` | `scripted` | PASS | 1.00 | [screenshot](examples/artifacts/20260724-004051-177323-pi-help-default/final.svg) / [video](examples/artifacts/20260724-004051-177323-pi-help-default/session.mp4) / [cast](examples/artifacts/20260724-004051-177323-pi-help-default/session.cast) / [screen_text](examples/artifacts/20260724-004051-177323-pi-help-default/final.txt) / [step_screenshots](examples/artifacts/20260724-004051-177323-pi-help-default/steps) |
| `pi-list` | `default` | `P0` | `scripted` | PASS | 1.00 | [screenshot](examples/artifacts/20260724-004054-385805-pi-list-default/final.svg) / [video](examples/artifacts/20260724-004054-385805-pi-list-default/session.mp4) / [cast](examples/artifacts/20260724-004054-385805-pi-list-default/session.cast) / [screen_text](examples/artifacts/20260724-004054-385805-pi-list-default/final.txt) / [step_screenshots](examples/artifacts/20260724-004054-385805-pi-list-default/steps) |
| `pi-version` | `default` | `P0` | `scripted` | PASS | 1.00 | [screenshot](examples/artifacts/20260724-004056-344321-pi-version-default/final.svg) / [video](examples/artifacts/20260724-004056-344321-pi-version-default/session.mp4) / [cast](examples/artifacts/20260724-004056-344321-pi-version-default/session.cast) / [screen_text](examples/artifacts/20260724-004056-344321-pi-version-default/final.txt) / [step_screenshots](examples/artifacts/20260724-004056-344321-pi-version-default/steps) |

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

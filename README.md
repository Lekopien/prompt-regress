# promptregress

Regression tests for prompts. Define cases in YAML, run them against one or more models, and fail your CI when quality drops.

## Why this exists
Prompts change, models get upgraded, and nobody notices a quality drop until users do. Unit tests for code are standard; this gives prompts the same safety net.

## Quick start
```bash
pip install -e .
export ANTHROPIC_API_KEY=sk-ant-...
promptregress examples/tests.yaml
```

## Check types
| type | meaning |
|---|---|
| `contains` / `not_contains` | case-insensitive substring |
| `regex` | `re.search` with DOTALL |
| `equals` | exact match after trim |
| `llm_judge` | plain-English criterion graded PASS/FAIL by a model |

## CI
`.github/workflows/prompt-tests.yml` runs the suite on every PR. Add `ANTHROPIC_API_KEY` as a repo secret. Use `--min-pass-rate 0.9` to tolerate small flakiness.

## Roadmap
- [ ] Cache outputs to cut cost on reruns
- [ ] Diff report vs. the last main-branch run
- [ ] Multi-provider support
- [ ] Latency and cost tracking per case

## License
MIT

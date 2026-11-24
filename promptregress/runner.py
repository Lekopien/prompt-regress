from dataclasses import dataclass, field
from pathlib import Path

import anthropic
import yaml

from .judges import CHECKS


@dataclass
class CaseResult:
    case_id: str
    model: str
    passed: bool
    output: str
    failures: list[str] = field(default_factory=list)


def load_suite(path: str) -> dict:
    return yaml.safe_load(Path(path).read_text())


def run_prompt(client: anthropic.Anthropic, model: str, prompt: str, system: str | None) -> str:
    kwargs = {"system": system} if system else {}
    msg = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
        **kwargs,
    )
    return msg.content[0].text


def run_suite(suite: dict, models: list[str] | None = None) -> list[CaseResult]:
    client = anthropic.Anthropic()
    models = models or suite.get("models", ["claude-sonnet-5-5"])
    system = suite.get("system")
    results: list[CaseResult] = []
    for model in models:
        for case in suite["cases"]:
            prompt = case["prompt"].format(**case.get("vars", {}))
            output = run_prompt(client, model, prompt, system)
            failures = []
            for check in case.get("checks", []):
                kind = check["type"]
                ok, why = CHECKS[kind](output, check["value"])
                if not ok:
                    failures.append(f"[{kind}] {why}")
            results.append(CaseResult(case["id"], model, not failures, output, failures))
    return results

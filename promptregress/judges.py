"""Check types: contains, not_contains, regex, equals, llm_judge."""
import re
from typing import Callable

import anthropic

JUDGE_MODEL_DEFAULT = "claude-sonnet-5-5"


def check_contains(output: str, value: str, **_) -> tuple[bool, str]:
    ok = value.lower() in output.lower()
    return ok, f"expected to contain {value!r}"


def check_not_contains(output: str, value: str, **_) -> tuple[bool, str]:
    ok = value.lower() not in output.lower()
    return ok, f"expected NOT to contain {value!r}"


def check_regex(output: str, value: str, **_) -> tuple[bool, str]:
    ok = re.search(value, output, re.S) is not None
    return ok, f"expected to match /{value}/"


def check_equals(output: str, value: str, **_) -> tuple[bool, str]:
    ok = output.strip() == value.strip()
    return ok, f"expected exact match {value!r}"


def check_llm_judge(output: str, value: str, judge_model: str = JUDGE_MODEL_DEFAULT, **_) -> tuple[bool, str]:
    """`value` is a plain-English criterion. The judge answers PASS or FAIL."""
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=judge_model,
        max_tokens=1000,
        system="You grade LLM outputs against a criterion. Reply with PASS or FAIL on the first line, then one short sentence of reasoning.",
        messages=[{"role": "user", "content": f"Criterion: {value}\n\nOutput to grade:\n{output}"}],
    )
    text = "".join(b.text for b in msg.content if b.type == "text").strip()
    return text.upper().startswith("PASS"), f"judge: {text[:160]}"


CHECKS: dict[str, Callable] = {
    "contains": check_contains,
    "not_contains": check_not_contains,
    "regex": check_regex,
    "equals": check_equals,
    "llm_judge": check_llm_judge,
}

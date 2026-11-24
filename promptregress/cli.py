import argparse
import json
import sys

from .runner import load_suite, run_suite


def main() -> None:
    p = argparse.ArgumentParser(prog="promptregress")
    p.add_argument("suite", help="Path to a YAML test suite")
    p.add_argument("--model", action="append", help="Override suite models (repeatable)")
    p.add_argument("--min-pass-rate", type=float, default=1.0, help="Fail if pass rate is below this (0-1)")
    p.add_argument("--json", dest="json_out", help="Write full results to this JSON file")
    args = p.parse_args()

    results = run_suite(load_suite(args.suite), args.model)
    passed = sum(r.passed for r in results)
    for r in results:
        mark = "PASS" if r.passed else "FAIL"
        print(f"{mark}  {r.model}  {r.case_id}")
        for f in r.failures:
            print(f"        - {f}")
    rate = passed / len(results) if results else 0
    print(f"\n{passed}/{len(results)} passed ({rate:.0%})")

    if args.json_out:
        with open(args.json_out, "w") as fh:
            json.dump([r.__dict__ for r in results], fh, indent=2)

    sys.exit(0 if rate >= args.min_pass_rate else 1)


if __name__ == "__main__":
    main()

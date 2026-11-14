#!/bin/bash
# Green gate for bottledmarbles-rest — run before every commit and by the daily publisher. Exit 0 = green.
set -euo pipefail
cd "$(dirname "$0")/.."
echo "== 1/4 unit tests"; python3 -m unittest discover -s tests -q
echo "== 2/4 landing pages match the build (tests/test_landing.py, above)"
echo "== 3/4 journal up to date"; python3 scripts/build_journal.py --check
echo "== 4/4 privacy/terms up to date"; python3 scripts/build_legal.py --check
echo GREEN

#!/bin/bash
# Green gate for bottledmarbles-rest — run before every commit and by the daily publisher. Exit 0 = green.
set -euo pipefail
cd "$(dirname "$0")/.."
echo "== 1/3 unit tests"; python3 -m unittest discover -s tests -q
echo "== 2/3 landing pages match the build (tests/test_landing.py, above)"
echo "== 3/3 journal up to date"; python3 scripts/build_journal.py --check
echo GREEN

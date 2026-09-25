#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if command -v python3 >/dev/null 2>&1; then
  exec python3 setup.py "$@"
fi
if command -v python >/dev/null 2>&1; then
  exec python setup.py "$@"
fi
echo "Python 3 not found. Install Python 3.13+ and retry."
exit 1

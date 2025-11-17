#!/usr/bin/env bash
# Heuristic scanner and sanitizer for likely exposed keys
set -euo pipefail
echo "[!] Scanning repo for secret-like patterns..."
patterns=("sk-" "AIza" "EAAl" "AKIA" "MINIO" "minioadmin" "postgresql://")
for p in "${patterns[@]}"; do
  echo "-> Searching for: $p"
  git grep -n --color=always "$p" || true
done

echo "[!] If you find matches, replace them and rotate keys immediately."
echo "Example replace (dangerous, inspect before running):"
echo "git grep -l 'sk-' | xargs -n1 sed -i 's/sk-[^[:space:]]\+/REDACTED_KEY/g'"

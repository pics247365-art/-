#!/bin/bash
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"

# Pull latest changes so every session starts fresh
git pull --rebase origin main 2>&1 || true

# Show current state
echo "Branch: $(git branch --show-current)"
echo "Last commit: $(git log -1 --oneline)"

#!/bin/bash
# Agent Pipeline Orchestrator
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="$SCRIPT_DIR/agent/scripts"

echo "=========================================="
echo "  Agent Pipeline Orchestrator"
echo "  Started: $(date)"
echo "=========================================="

AGENTS=("architect" "engineer" "mason" "coder" "deliverer")

for agent in "${AGENTS[@]}"; do
    echo "--- Running ${agent^} ---"
    bash "$SCRIPTS_DIR/run_${agent}.sh" || {
        echo "Pipeline stopped at ${agent}"
        exit 1
    }
done

echo "=========================================="
echo "  Pipeline Complete!"
echo "=========================================="

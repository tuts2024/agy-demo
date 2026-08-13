#!/usr/bin/env bash
# ==============================================================================
# Helper to create a fresh, open GitHub Pull Request for live presentations.
# Resets base code on main, pushes feature branch, and opens PR on GitHub.
# ==============================================================================

set -e

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$WORKSPACE_DIR"

python3 create_demo_pr.py

#!/usr/bin/env bash
# ==============================================================================
# Autonomous SDLC Code Review & Self-Healing Remediation Demo Launcher
# Powered by Jetski AI / Gemini Agent
# ==============================================================================

set -e

PORT=${1:-8085}
WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$WORKSPACE_DIR"

echo "======================================================================"
echo "🚀 Initializing Autonomous SDLC Review & Remediation Demo..."
echo "======================================================================"
echo "📍 Workspace: $WORKSPACE_DIR"
echo "🌐 UI Port:   http://localhost:$PORT/"
echo ""

# Reset state
python3 orchestrate_review.py --reset

echo "✨ Starting live interactive web dashboard..."
echo "👉 Open your browser to: http://localhost:$PORT/"
echo ""
echo "Press Ctrl+C to stop the demo server."
echo "======================================================================"

python3 orchestrate_review.py --serve --port "$PORT"

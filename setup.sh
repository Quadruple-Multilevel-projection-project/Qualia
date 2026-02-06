#!/usr/bin/env bash
set -euo pipefail

echo "🧭 Setting up Quantum Orchestrator workspace..."
mkdir -p core bridge manifest

echo "✅ Workspace ready."
echo "🚀 Running Quantum Orchestrator..."
python quantum_orchestrator.py

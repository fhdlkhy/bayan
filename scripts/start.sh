#!/usr/bin/env bash
set -euo pipefail

# Helper to run the app locally inside container or dev environment
if [ -f ".env" ]; then
  # load env file (simple)
  export $(grep -v '^#' .env | xargs)
fi

exec streamlit run app.py --server.port=8501 --server.headless=true

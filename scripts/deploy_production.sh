#!/usr/bin/env bash
set -e

echo "Starting production deployment..."
mkdir -p production_deploy
cp app.py requirements.txt .gitignore production_deploy/ 2>/dev/null || true
cp -R tests production_deploy/ 2>/dev/null || true
if [ -n "$PROD_DEPLOY_KEY" ]; then
  echo "Using production deploy key"
fi

echo "Flask app deployed to production_deploy/"

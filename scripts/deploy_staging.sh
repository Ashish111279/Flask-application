#!/usr/bin/env bash
set -e

echo "Starting staging deployment..."
mkdir -p staging_deploy
cp app.py requirements.txt .gitignore staging_deploy/ 2>/dev/null || true
cp -R tests staging_deploy/ 2>/dev/null || true
if [ -n "$STAGING_DEPLOY_KEY" ]; then
  echo "Using staging deploy key"
fi

echo "Flask app deployed to staging_deploy/"

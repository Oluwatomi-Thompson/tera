#!/usr/bin/env bash
# Render build step: Python deps, then the compiled Tailwind CSS.
set -o errexit

pip install -r requirements.txt

if command -v npm >/dev/null 2>&1; then
  # --include=dev because tailwindcss is a devDependency.
  if [ -f package-lock.json ]; then
    npm ci --include=dev
  else
    npm install --include=dev
  fi
  npm run build-css
else
  echo "npm not found on this host; using the committed app/static/css/output.css"
fi

# Fail the build loudly (not the site silently) if there is no stylesheet.
test -s app/static/css/output.css || { echo "ERROR: app/static/css/output.css is missing or empty"; exit 1; }

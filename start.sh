#!/usr/bin/env bash
# Render start step. Free web services have no pre-deploy hook or shell,
# so migrations, seeding and the admin account all happen here. Every
# command is idempotent, so restarts and spin-ups are safe.
set -o errexit
export FLASK_APP=wsgi.py
flask db upgrade
flask seed-db
if [ -n "${ADMIN_EMAIL:-}" ] && [ -n "${ADMIN_PASSWORD:-}" ]; then
  flask create-admin --email "$ADMIN_EMAIL" --password "$ADMIN_PASSWORD"
fi
exec gunicorn wsgi:app --bind 0.0.0.0:${PORT:-10000} --workers 2 --access-logfile -

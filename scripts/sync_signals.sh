#!/usr/bin/env bash
set -euo pipefail

: "${SSH_KEY_PATH:?Missing SSH_KEY_PATH}"
: "${RESEARCH_HOST:?Missing RESEARCH_HOST}"
: "${RESEARCH_USER:?Missing RESEARCH_USER}"
: "${RESEARCH_REMOTE_DIR:?Missing RESEARCH_REMOTE_DIR}"
: "${SIGNAL_DIR:?Missing SIGNAL_DIR}"

chmod 400 "$SSH_KEY_PATH" || true
mkdir -p "$SIGNAL_DIR"

rsync -avz \
  -e "ssh -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new -i $SSH_KEY_PATH" \
  "${RESEARCH_USER}@${RESEARCH_HOST}:${RESEARCH_REMOTE_DIR}/" \
  "$SIGNAL_DIR"/

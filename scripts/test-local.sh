#!/usr/bin/env bash
# Lightweight wrapper kept for backwards compatibility.
# It delegates to `scripts/test.sh --local` so the real logic lives in one file.
exec ./scripts/test.sh --local "$@"

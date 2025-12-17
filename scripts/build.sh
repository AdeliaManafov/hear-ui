#! /usr/bin/env sh

# Purpose:
#  - Build project images (or frontend) using the `docker-compose.yml` setup.
#
# What it does:
#  - Uses `TAG` (required) and optional `FRONTEND_ENV` to control build-time
#    configuration and then runs `docker-compose build`.
#
# When to use:
#  - Run this locally to build images before testing, or in CI when preparing
#    images for tagging. The script does not push images.

# Exit in case of error
set -e

TAG=${TAG?Variable not set} \
FRONTEND_ENV=${FRONTEND_ENV-production} \
docker-compose \
-f docker/docker-compose.yml \
--env-file "$PWD/.env" \
build

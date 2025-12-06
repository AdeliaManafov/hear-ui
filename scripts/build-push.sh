#! /usr/bin/env sh

# Purpose:
#  - Build project images (delegates to `build.sh`) and push them to a Docker
#    registry using `docker-compose push`.
#
# Requirements / caution:
#  - `TAG` must be set and images should be tagged accordingly.
#  - You must be logged in to the target registry (e.g. `docker login`).
#  - This script will upload images to a registry — review before running
#    to avoid accidental pushes to production registries.

# Exit in case of error
set -e

TAG=${TAG?Variable not set} \
FRONTEND_ENV=${FRONTEND_ENV-production} \
sh ./scripts/build.sh

docker-compose -f docker-compose.yml push

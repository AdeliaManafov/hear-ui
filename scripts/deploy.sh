#! /usr/bin/env sh

# Purpose:
#  - Prepare a Docker stack deployment from `docker-compose.yml` and deploy it
#    to a Docker Swarm (or compatible) manager.
#
# What it does:
#  - Reads mandatory environment variables (`DOMAIN`, `STACK_NAME`, `TAG`).
#  - Renders `docker-compose.yml` into a deployable `docker-stack.yml` via
#    `docker-compose config` and runs `docker-auto-labels` to add labels.
#  - Calls `docker stack deploy` with `--with-registry-auth` to pull images
#    from a registry requiring authentication.
#
# Requirements / caution:
#  - Only use this when you intend to deploy to a Docker Swarm or compatible
#    orchestrator. This script can affect production systems — review before
#    running. Ensure you have appropriate permissions and registry credentials
#    configured (DOCKER config / login).

# Exit on error
set -e

DOMAIN=${DOMAIN?Variable not set} \
STACK_NAME=${STACK_NAME?Variable not set} \
TAG=${TAG?Variable not set} \
docker-compose \
-f docker-compose.yml \
config > docker-stack.yml

docker-auto-labels docker-stack.yml

docker stack deploy -c docker-stack.yml --with-registry-auth "${STACK_NAME?Variable not set}"

#!/bin/bash
set -Eeuxo pipefail

docker-compose -f docker-compose.portal.yaml -f docker-compose.jd.yaml down --remove-orphans
docker-compose -f docker-compose.portal.yaml -f docker-compose.jd.yaml up
docker-compose -f docker-compose.portal.yaml -f docker-compose.jd.yaml logs -f

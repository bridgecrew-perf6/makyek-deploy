#!/bin/bash
set -Eeuxo pipefail
cd -- "$( dirname -- "${BASH_SOURCE[0]}" )"

docker-compose -f docker-compose.portal.yaml -f docker-compose.jd.yaml down --remove-orphans
docker-compose -f docker-compose.portal.yaml -f docker-compose.jd.yaml up -d
docker-compose -f docker-compose.portal.yaml -f docker-compose.jd.yaml logs -f

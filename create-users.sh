#!/bin/bash
set -Eeuxo pipefail

function docker-exec() {
    docker-compose -f docker-compose.portal.yaml -f docker-compose.jd.yaml exec portal $@
}

docker-exec npm run cli -- DI.models.User.createUserAsync admin admin 1000 admin admin
docker-exec npm run cli -- DI.models.User.createUserAsync user1 admin 1000 user1 student
docker-exec npm run cli -- DI.models.User.createUserAsync user2 admin 1000 user2 student
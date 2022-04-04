example configs for running inside docker-compose

## Requirements

Tested on:
- Kali rolling (Linux kernel 5.16.0)
- Docker 20.10.11
- Docker Compose 1.29.2

## Usage

Build containers:
```shell
(cd ../makyek-portal && docker-compose build)
(cd ../makyek-jd && docker-compose build)
```

Start server:
```shell
./start-debug.sh
./create-users.sh # creates some test user
```

Portal is hosted at http://localhost:8888.

Reset data (dangerous!):
```shell
docker-compose -f docker-compose.portal.yaml -f docker-compose.jd.yaml down --remove-orphans
rm .persistence
```

## Notes

- Some containers will restart a few times before all their dependencies are up. This is expected. 
- The portal and all the jd-compile containers must share exactly the same view of compiler list
- All the jd-match containers must be able to run any of the target executables
- If rabbitmq restarts, jd-compile and jd-match containers might stall, causing all jobs to stuck in pending status. In such case, please manually restart all jd-compile and jd-match containers. 

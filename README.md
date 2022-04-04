example configs for running inside docker-compose

## Usage

Tested on:
- Kali rolling (Linux kernel 5.16.0)
- Docker 20.10.11
- Docker Compose 1.29.2

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

Reset data (dangerous!):
```shell
docker-compose -f docker-compose.portal.yaml -f docker-compose.jd.yaml down --remove-orphans
rm .persistence
```

Note:
- Some containers will restart a few times before all their dependencies are up. This is expected. 

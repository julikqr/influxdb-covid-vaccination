# influxdb-covid-vaccination

docker run --name influxdb -p 8086:8086 -v C:\Users\julia\docker-influx-data:/root/.influxdbv2 influxdb:2.0.4

## Prerequisites
1. Install docker

## How to run this project
Run the following commands in your console
1. Run the following command to start influxdb server
```bash
docker run -p 8086:8086 -e DOCKER_INFLUXDB_INIT_USERNAME=my-user -e DOCKER_INFLUXDB_INIT_MODE=setup -e DOCKER_INFLUXDB_INIT_PASSWORD=my-password -e DOCKER_INFLUXDB_INIT_ORG=my-org -e DOCKER_INFLUXDB_INIT_BUCKET=my-bucket influxdb:2.0.4
``` 
2. Navigate to project directory and run main py
```
./main.py
```


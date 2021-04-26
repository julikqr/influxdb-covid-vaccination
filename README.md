# influxdb-covid-vaccination
This Project is using Python 3.8.5 and InfluxDB 2.0.4. A Docker Container is used to run the InfluxDB Server.

docker run --name influxdb -p 8086:8086 -v C:\Users\julia\docker-influx-data:/root/.influxdbv2 influxdb:2.0.4
https://hub.docker.com/_/influxdb
## Prerequisites
1. Install Docker Desktop from https://www.docker.com/get-started (Maybe a Restart is needed to run Docker commands from console)
2. Install Python dependencies from `requirements.txt`
## How to run this project
Run the following commands in your console.
Make sure that port 8086 is not in use.

1. Run the command to start influxdb server

```bash
docker run -p 8086:8086 -e DOCKER_INFLUXDB_INIT_MODE=setup -e DOCKER_INFLUXDB_INIT_USERNAME=my-user -e DOCKER_INFLUXDB_INIT_PASSWORD=my-password -e DOCKER_INFLUXDB_INIT_ORG=my-org -e DOCKER_INFLUXDB_INIT_BUCKET=my-bucket -e DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my-super-secret-auth-token influxdb:2.0.4
``` 
2. Navigate to project directory and run `main.py`
```
python ./main.py
```


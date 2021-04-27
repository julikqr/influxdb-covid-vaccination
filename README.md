# InfluxDB Covid Vaccination Data with Python
This Project is using Python 3.8.5 and InfluxDB 2.0.4. A Docker Container is used to run the InfluxDB Server. The use of a Python virtual environment is recommended to install all Python dependencies.

---

More Information about Influx:

https://www.influxdata.com/

https://hub.docker.com/_/influxdb

https://github.com/influxdata/influxdb-client-python

Covid vaccination data origin:

https://impfdashboard.de/daten

---

## Prerequisites
1. Install Python from https://www.python.org/
2. Install Docker Desktop from https://www.docker.com/get-started (Maybe a Restart is needed to run Docker commands from console)
3. Clone this repository and navigate to the project directory
4. Optional: Create a virtual environment and run the `activate.bat` script of your virtual environment
```bash
python -m venv venv
.\venv\Scripts\activate.bat
```
5. Install Python dependencies from `requirements.txt`
```bash
pip install -r requirements.txt
```
## How to run this project
Run the following commands in your console.
Make sure that port 8086 is not in use.

1. Run the command to start influxdb server (docker must be running)

```bash
docker run -p 8086:8086 -e DOCKER_INFLUXDB_INIT_MODE=setup -e DOCKER_INFLUXDB_INIT_USERNAME=my-user -e DOCKER_INFLUXDB_INIT_PASSWORD=my-password -e DOCKER_INFLUXDB_INIT_ORG=my-org -e DOCKER_INFLUXDB_INIT_BUCKET=my-bucket -e DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my-super-secret-auth-token influxdb:2.0.4
``` 
2. Navigate to project directory and run `main.py`
```
python ./main.py
```

---

## Connect to the influx CLI
You can use the influx CLI to commincate with the influxDB Server. The CLI is started within the same Docker Container as influxDB.
```bash
docker exec -it <Container Name here> /bin/bash
```
Show a list of all running containers
```bash
docker container ls
```

---

docker run --name influxdb -p 8086:8086 -v C:\Users\julia\docker-influx-data:/root/.influxdbv2 influxdb:2.0.4


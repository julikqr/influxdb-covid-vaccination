# InfluxDB 2.0.4 Covid Vaccination Data with Python
This Project is using Python 3.8.5 and InfluxDB 2.0.4. A Docker Container is used to run the InfluxDB Server. The use of a Python virtual environment is recommended to install all Python dependencies.

This project writes and reads Covid Vaccination Data to InfluxDB database using the influxdb-client and pandas module. The data is then visualized with the matplotlib.

---

More Information about Influx:

https://www.influxdata.com/

https://hub.docker.com/_/influxdb

https://github.com/influxdata/influxdb-client-python

Covid vaccination data origin:

https://impfdashboard.de/daten

---

## Prerequisites
Works on Windows, Mac and Linux. Docker installation on Linux is different, see here [Docker Linux](https://docs.docker.com/engine/install/ubuntu/). Commands were tested on Windows, you might have to adapt the paths to fit your system. 
1. Install Python from https://www.python.org/
2. Install Docker Desktop from https://www.docker.com/get-started (Maybe a Restart is needed to run Docker commands from console)
3. Clone this repository and **navigate to the project directory**
4. Optional: Create a virtual environment (venv) and run the `activate.bat` script to activate your venv
```bash
python -m venv venv             # create your venv
.\venv\Scripts\activate.bat     # activate your venv
```
&ensp;&ensp;&ensp; Info: You can deactivate your venv with the following command (don't do that now)
```bash
deactivate
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
python src/main.py
```
### How to run unittests

There are two unittests in this project: `test_model.py` and `test_view.py`. One tests the model and one the view. There's no test for the `controller` as its only controlling `model` and `view`. You can run unittests with:
```bash
python ./src/test_model.py          # runs unittest for model
python ./src/test_view.py           # runs unittest for view
```


---

## Connect to the influx CLI
You can use the influx CLI to communicate with the influxDB Server. The CLI is started within the same Docker Container as influxDB.
```
docker exec -it <Docker container name here> /bin/bash
```
Enter influx to see a list of available commands
```bash
influx
```

---
Info: Show a list of all running Docker containers with their names
```bash
docker container ls
```

---




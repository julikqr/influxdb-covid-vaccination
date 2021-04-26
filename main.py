from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


token = "EfiBO99h-DYKYR2X71YZZH1lC7f85ZUiG4iIhk3vpqzJ6TV7gMcKGMzjXTJnLfoJZtwIebajQanlhItnP_qPqA=="
org = "jul"
bucket = "buc"

client = InfluxDBClient(url="http://localhost:8086", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)

data = "mem,host=host1 used_percent=23.43234543"
write_api.write(bucket, org, data)

print("ende")

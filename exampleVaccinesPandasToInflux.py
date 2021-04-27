from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timedelta
from pytz import UTC
import pandas as pd

# simple exampe of how to write a pandas dataframe to influxdb


# setup authentication
token = "my-super-secret-auth-token"
org = "my-org"
bucket = "vaccine-bucket"

client = InfluxDBClient(url="http://localhost:8086", token=token)

_write_client = client.write_api(write_options=WriteOptions(batch_size=1000,
                                                            flush_interval=10_000,
                                                            jitter_interval=2_000,
                                                            retry_interval=5_000))
_query_api = client.query_api()

df = pd.read_csv(".\data\germany_deliveries_timeseries_v2.csv", sep=';')
df["date"] = df["date"].str.replace(".", "-")
df["date"] = df["date"].apply(lambda x: x[6:10] + x[2:6] + x[0:2])
df.set_index("date", inplace=True)

print(df)
if(False):
    _write_client.write(bucket, org, record=df, data_frame_measurement_name='vaccine',
                        data_frame_tag_columns=['region', 'impfstoff'])

query = f'''from(bucket:"{bucket}")
    |> range(start: -5d)
    |> filter(fn: (r) =>
        r.region == "DE-BW" and
        r._field == "dosen"
    )
'''
print(query)

tables = _query_api.query(query, org=org)
for table in tables:
    print()
    for record in table.records:
        print(
            f'Time: {record.values["_time"]}; region: {record.values["region"]}; impfstoff: {record.values["impfstoff"]}; Dosen: {record.values["_value"]}')

print("end")
_write_client.close()
client.close()

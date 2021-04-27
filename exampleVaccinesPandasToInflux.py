from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd

# simple example of how to write a pandas dataframe to influxdb and then query the data

# covid data urls
url_vaccine_deliveries = "https://impfdashboard.de/static/data/germany_deliveries_timeseries_v2.tsv"

# setup authentication
token = "my-super-secret-auth-token"
org = "my-org"
bucket = "my-bucket"

client = InfluxDBClient(url="http://localhost:8086", token=token)
_query_api = client.query_api()

#df = pd.read_csv(".\data\germany_deliveries_timeseries_v2.csv", sep=';')
#df["date"] = df["date"].str.replace(".", "-")
#df["date"] = df["date"].apply(lambda x: x[6:10] + x[2:6] + x[0:2])


writedata = False
print(f'********** Write Data is set to {writedata} ************************')
if(writedata):
    _write_client = client.write_api(write_options=WriteOptions(batch_size=1000,
                                                                flush_interval=10_000,
                                                                jitter_interval=2_000,
                                                                retry_interval=5_000))
    df = pd.read_csv(url_vaccine_deliveries, sep='\t')
    df.set_index("date", inplace=True)
    print(df)
    result = _write_client.write(bucket, org, record=df, data_frame_measurement_name='vaccine',
                                 data_frame_tag_columns=['region', 'impfstoff'])
    print("Data was written to influx - Closing _write_client now")
    _write_client.close()

# query all deliveries of DE-BW from the last 90 days
query = f'''from(bucket:"{bucket}")
    |> range(start: -90d)
    |> filter(fn: (r) =>
        r.region == "DE-BW" and
        r._field == "dosen"
    )
'''
print(query)
tables = _query_api.query(query, org=org)

# print results of the query
for table in tables:
    print()
    for record in table.records:
        print(
            f'Time: {record.values["_time"]}; region: {record.values["region"]}; impfstoff: {record.values["impfstoff"]}; Dosen: {record.values["_value"]}')

# close database connection
client.close()

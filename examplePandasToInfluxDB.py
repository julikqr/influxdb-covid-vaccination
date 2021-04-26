from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timedelta
from pytz import UTC
import pandas as pd

# simple exampe of how to write a pandas dataframe to influxdb


# setup authentication
token = "my-super-secret-auth-token"
org = "my-org"
bucket = "my-bucket"

client = InfluxDBClient(url="http://localhost:8086", token=token)

_write_client = client.write_api(write_options=WriteOptions(batch_size=1000,
                                                            flush_interval=10_000,
                                                            jitter_interval=2_000,
                                                            retry_interval=5_000))

_now = datetime.now(UTC)
_data_frame = pd.DataFrame(data=[["coyote_creek", 1.0], ["coyote_creek", 2.0]],
                           index=[_now, _now + timedelta(hours=1)],
                           columns=["location", "water_level"])

print(_data_frame)
_write_client.write(bucket, org, record=_data_frame, data_frame_measurement_name='h20_feet',
                    data_frame_tag_columns=['location'])

_write_client.close()

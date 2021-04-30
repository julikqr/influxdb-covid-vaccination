from datetime import datetime
import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

from controller import Controller


def main():
    controller = Controller()
    controller.start_gui()

    # setup authentication
    #token = "my-super-secret-auth-token"
    #org = "my-org"
    #bucket = "my-bucket"

    #client = InfluxDBClient(url="http://localhost:8086", token=token)

    # write_client = client.write_api(write_options=WriteOptions(batch_size=500,
    #                                                           flush_interval=10_000,
    #                                                           jitter_interval=2_000,
    #                                                           retry_interval=5_000,
    #                                                           max_retries=5,
    #                                                           max_retry_delay=30_000,
    #                                                           exponential_base=2))
    #data = "mem,host=host1 used_percent=23.43234543"
    #write_api.write(bucket, org, data)

    #df = pd.read_csv(".\data\germany_deliveries_timeseries_v2.csv", sep=';')
    #df["date"] = df["date"].str.replace(".", "-")
    #df.set_index("date", inplace=True)
    # write_client.write(bucket, org, record=df, data_frame_measurement_name="vaccine_deliveries",
    #                   data_frame_tag_columns=['region', 'impfstoff'])
    #dt = datetime.now()

    #_now = datetime.now()
    # _data_frame = pd.DataFrame(data=[["coyote_creek", 1.0], ["coyote_creek", 2.0]],
    #                           index=[_now, _now],
    #                           columns=["location", "water_level"])

    # write_client.write("my-bucket", "my-org", record=_data_frame, data_frame_measurement_name='h2o_feet',
    #                   data_frame_tag_columns=['location'])
    # print("ende")


if __name__ == "__main__":
    print("Hello World")
    main()

from influxdb_client import InfluxDBClient
import pandas as pd
from datetime import datetime
from pytz import UTC


class Model:
    def __init__(self, token="my-super-secret-auth-token", org="my-org", bucket="my-bucket", url="http://localhost:8086"):
        # self.client
        self.token = token
        self.bucket = bucket
        self.org = org
        self.dburl = url

        self.url_vaccine_deliveries = "https://impfdashboard.de/static/data/germany_deliveries_timeseries_v2.tsv"

    def connect_to_db(self):
        self.client = InfluxDBClient(
            url=self.dburl, token=self.token, org=self.org)
        return self.test_connection()

    def test_connection(self):
        try:
            test_query = f'''from(bucket:"{self.bucket}")
                |> range(start: -1d)
            '''
            self.client.query_api().query(query=test_query)
            return True
        except Exception as exc:
            print("Connection failed:")
            print(exc)
            return False

    def create_vaccine_deliveries(self):
        created = False
        try:
            write_client = self.client.write_api()
            df = pd.read_csv(self.url_vaccine_deliveries, sep='\t')
            df.set_index("date", inplace=True)
            write_client.write(self.bucket, record=df, data_frame_measurement_name='vaccine_delivery',
                               data_frame_tag_columns=['region', 'impfstoff'])
            write_client.close()
            created = True
        except Exception as exc:
            print(exc)
        return created
        print("Data Created; Closed client")

    def delete(self, measurement):
        deleted = False
        try:
            delete_client = self.client.delete_api()
            start = "2020-01-01T00:00:00Z"
            stop = datetime.now(UTC)
            delete_client.delete(
                start, stop, f'_measurement={measurement}', self.bucket, self.org)
            deleted = True
        except Exception as exc:
            print(exc)
        return deleted

    def execute_query(self, button):
        return f"Execute {button} query"

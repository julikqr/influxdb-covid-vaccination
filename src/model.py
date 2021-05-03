from influxdb_client import InfluxDBClient
import pandas as pd
from datetime import datetime
from pytz import UTC


class Model:
    def __init__(self, token="my-super-secret-auth-token", org="my-org", bucket="my-bucket", url="http://localhost:8086"):
        self.token = token
        self.bucket = bucket
        self.org = org
        self.dburl = url
        self.url_vaccine_deliveries = "https://impfdashboard.de/static/data/germany_deliveries_timeseries_v2.tsv"
        self.start = "2020-01-01T00:00:00Z"
        self.stop = datetime.now(UTC).isoformat()

        self.query_TestConnectionQuery = f'''from(bucket:"{self.bucket}")
                    |> range(start: -1d)
        '''
        self.query_CumulativeGroupByVaccine = f'''from(bucket:"{self.bucket}")
                    |> range(start: {self.start}, stop: {self.stop})
                    |> group(columns: ["impfstoff"], mode:"by")
                    |> filter(fn: (r) => r.region == "DE-BW")
                    |> cumulativeSum()
        '''
        self.query_VaccinesMean14d = f'''from(bucket: "{self.bucket}")
                    |> range(start: {self.start}, stop: {self.stop})
                    |> group(columns: ["impfstoff"], mode: "by")
                    |> aggregateWindow(every: 14d, fn: mean, createEmpty: false)
        '''
        self.query_StatesWithMostVaccines = f'''from(bucket: "{self.bucket}")
                    |> range(start: {self.start}, stop: {self.stop})
                    |> group(columns: ["region"])
                    |> cumulativeSum()
                    |> max()
        '''
        self.query_VaccinesInDEBW = f'''from(bucket:"{self.bucket}")
                    |> range(start: {self.start}, stop: {self.stop})
                    |> filter(fn: (r) =>
                        r.region == "DE-BW" and
                        r._field == "dosen"
                    )
        '''

    def connect_to_db(self):
        print(f"Connecting to {self.dburl} InfluxDB...")
        self.client = InfluxDBClient(
            url=self.dburl, token=self.token, org=self.org)
        return self._test_connection()

    def _test_connection(self):
        try:
            self.client.query_api().query(query=self.query_TestConnectionQuery)
            print("Connected")
            return True
        except Exception as exc:
            print("Connection failed:")
            print(exc)
            return False

    def create_vaccine_deliveries(self):
        created = False
        result_df = self._execute_query(self.query_VaccinesInDEBW)
        if(result_df.empty):
            try:
                write_client = self.client.write_api()
                #df = pd.read_csv(self.url_vaccine_deliveries, sep='\t')
                df = pd.read_csv('data\vaccine_deliveries.tsv', sep='\t')
                df.to_csv("out.tsv", sep='\t', index=False)
                df.set_index("date", inplace=True)
                write_client.write(self.bucket, record=df, data_frame_measurement_name='vaccine_delivery',
                                   data_frame_tag_columns=['region', 'impfstoff'])
                write_client.close()
                created = True
            except Exception as exc:
                print(exc)
            print("Data Created; Closed client")
        else:
            created = True
        return created

    def read_vaccine_deliveries_debw(self):
        df = self._execute_query(self.query_VaccinesInDEBW)
        if not df.empty:
            df = df.rename(
                columns={"_time": "x_axis", "_value": "y_axis", "impfstoff": "line_name"})
        return df

    def read_states_most_vaccines(self):
        df = self._execute_query(self.query_StatesWithMostVaccines)
        if not df.empty:
            df = df.rename(columns={"region": "x_axis", "_value": "y_axis"})
        return df

    def read_vaccine_mean(self):
        df = self._execute_query(self.query_VaccinesMean14d)
        if not df.empty:
            df = df.rename(
                columns={"_time": "x_axis", "_value": "y_axis", "impfstoff": "line_name"})
        return df

    def read_cumulated_deliveries_by_vaccine(self):
        df = self._execute_query(self.query_CumulativeGroupByVaccine)
        if not df.empty:
            df = df.rename(
                columns={"_time": "x_axis", "_value": "y_axis", "impfstoff": "line_name"})
        return df

    def _execute_query(self, query):
        try:
            query_client = self.client.query_api()
            return query_client.query_data_frame(query)
        except Exception as exc:
            print(exc)
            return pd.DataFrame()

    def delete(self, measurement):
        deleted = False
        try:
            delete_client = self.client.delete_api()
            stop = datetime.now(UTC)
            delete_client.delete(
                self.start, stop, f'_measurement={measurement}', self.bucket, self.org)
            deleted = True
        except Exception as exc:
            print(exc)
        return deleted

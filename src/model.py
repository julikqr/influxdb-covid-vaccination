"""Model
        * This file contains the Model
        * handle database communication
        * read, write and delete data from/to database

    Attributes:
        * name: Julian S
        * date: 03.05.2021
        * version: 0.0.1 Beta - free
"""

from influxdb_client import InfluxDBClient
import pandas as pd
from datetime import datetime
from pytz import UTC
import os
from pathlib import Path


class Model:
    def __init__(self, token="my-super-secret-auth-token", org="my-org", bucket="my-bucket", url="http://localhost:8086"):
        """__init__
            * initialize authentication data
            * initialize flux queries
        Args:
            token (str, optional): InfluxDB Authentication token. Defaults to "my-super-secret-auth-token".
            org (str, optional): InfluxDB default organization. Defaults to "my-org".
            bucket (str, optional): InfluxDB default bucket. Defaults to "my-bucket".
            url (str, optional): InfluxDB server adress. Defaults to "http://localhost:8086".
        """
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
        """connect_to_db
            * set up InfluxDB Client. Used to communicate with InfluxDB
            * test connection 
        Returns:
            bool: Connection succesful or not
        """
        print(f"Connecting to {self.dburl} InfluxDB...")
        self.client = InfluxDBClient(
            url=self.dburl, token=self.token, org=self.org)
        return self._test_connection()

    def _test_connection(self):
        """test_connection
            * test connection to InfluxDB
        Returns:
            bool: Connection working or not
        """
        try:
            self.client.query_api().query(query=self.query_TestConnectionQuery)
            return True
        except Exception as exc:
            return False

    def create_vaccine_deliveries(self):
        """create_vaccine_deliveries
            * reads data from csv
            * writes data to InfluxDB
        Returns:
            bool: Data was written succesful or not
        """
        created = False
        result_df = self._execute_query(self.query_VaccinesInDEBW)
        if(result_df.empty):
            try:
                write_client = self.client.write_api()
                #df = pd.read_csv(self.url_vaccine_deliveries, sep='\t')
                vaccines_csv_path = self._get_data_directory_file(
                    'vaccine_deliveries.tsv')
                df = pd.read_csv(vaccines_csv_path, sep='\t')
                #df.to_csv("out.tsv", sep='\t', index=False)
                df.set_index("date", inplace=True)
                write_client.write(self.bucket, record=df, data_frame_measurement_name='vaccine_delivery',
                                   data_frame_tag_columns=['region', 'impfstoff'])
                write_client.close()
                created = True
            except Exception as exc:
                pass
        else:
            created = True
        return created

    def read_vaccine_deliveries_debw(self):
        """read vaccine deliveries from DE-BW
            * execute flux query
            * rename columns to fit plot function of View
        Returns:
            Pandas Datframe: A Dataframe with result data
        """
        df = self._execute_query(self.query_VaccinesInDEBW)
        if not df.empty:
            df = df.rename(
                columns={"_time": "x_axis", "_value": "y_axis", "impfstoff": "line_name"})
        return df

    def read_states_most_vaccines(self):
        """read vaccine deliveries from DE-BW
            * execute flux query
            * rename columns to fit plot function of View
        Returns:
            Pandas Datframe: A Dataframe with result data
        """
        df = self._execute_query(self.query_StatesWithMostVaccines)
        if not df.empty:
            df = df.rename(columns={"region": "x_axis", "_value": "y_axis"})
        return df

    def read_vaccine_mean(self):
        """read vaccine deliveries from DE-BW
            * execute flux query
            * rename columns to fit plot function of View
        Returns:
            Pandas Datframe: A Dataframe with result data
        """
        df = self._execute_query(self.query_VaccinesMean14d)
        if not df.empty:
            df = df.rename(
                columns={"_time": "x_axis", "_value": "y_axis", "impfstoff": "line_name"})
        return df

    def read_cumulated_deliveries_by_vaccine(self):
        """read vaccine deliveries from DE-BW
            * execute flux query
            * rename columns to fit plot function of View
        Returns:
            Pandas Datframe: A Dataframe with result data
        """
        df = self._execute_query(self.query_CumulativeGroupByVaccine)
        if not df.empty:
            df = df.rename(
                columns={"_time": "x_axis", "_value": "y_axis", "impfstoff": "line_name"})
        return df

    def _execute_query(self, query):
        """execute flux query
            * execute a given flux query
        Args:
            query (str): flux query

        Returns:
            Pandas Dataframe: A Dataframe with the result. Might be an empty Datframe
        """
        try:
            query_client = self.client.query_api()
            return query_client.query_data_frame(query)
        except Exception as exc:
            return pd.DataFrame()

    def delete(self, measurement):
        """delete given measurement

        Args:
            measurement (str): Name of measurement to delete

        Returns:
            bool: Return True if deleting was succesfull
        """
        deleted = False
        try:
            delete_client = self.client.delete_api()
            stop = datetime.now(UTC)
            delete_client.delete(
                self.start, stop, f'_measurement={measurement}', self.bucket, self.org)
            deleted = True
        except Exception as exc:
            pass
        return deleted

    def _get_data_directory_file(self, filename):
        """get_data_directory_file
            * gets full path of a file inside data directory
        Args:
            filename (str): String of a filename inside data directory
        Returns:
            str: full path to given file as a str 
        """
        if type(filename) is str:
            curdir = os.path.dirname(os.path.realpath(__file__))
            return Path(curdir).parents[0] / 'data' / filename
        else:
            raise TypeError()
            return ""

"""TestModel
        * Unittest
        * This file contains the TestModel
        * testing database read, write and delete

    Attributes:
        * name: Julian S
        * date: 03.05.2021
        * version: 0.0.1 Beta - free
"""

import unittest
from model import Model
import pandas as pd
import pandas.testing as pd_testing


class TestModel(unittest.TestCase):
    """TestView
        * Unittest for model.py
        * This unittest needs a connection to InfluxDB as it is also testing write/read and delte
    Args:
        unittest (unittest): TestModel inherits from unittest to contain all of its functionity 
    """

    @classmethod
    def setUpClass(cls):
        """setUpClass
            * create a model to test
            * connect model to database
            * create data
        """
        cls.model = Model()
        cls.model.connect_to_db()
        cls.model.create_vaccine_deliveries()

    def test_client_db_connectiont(self):
        """test_cluent_db_connection
            * connect to InfluxDB with wrong url
            * connect to InfluxDB with wrong token
            * connect to InfluxDB with wrong bucket
            * connect to InfluxDB with correct authentication
        """
        model = Model(url="CompltelyWrongUrl")
        self.assertEqual(model.connect_to_db(), False)

        model = Model(token="wrongToken")
        self.assertEqual(model.connect_to_db(), False)

        model = Model(bucket="wrongBucket")
        self.assertEqual(model.connect_to_db(), False)

        model = Model(url="http://localhost:8086",
                      token="my-super-secret-auth-token", org="my-org", bucket="my-bucket")
        self.assertEqual(model.connect_to_db(), True)

    def test_query_vaccine_deliveries_debw(self):
        """Test vaccine delivery of DE-BW query
            * compare expected dataframe to result dataframe
        """
        result_df = self.model.read_vaccine_deliveries_debw().head()
        result_df = result_df[['y_axis', '_field',
                               '_measurement', 'line_name', 'region']]
        result_df['y_axis'] = result_df['y_axis'].astype('int64')
        expected_df = pd.DataFrame({
            'y_axis': [48000, 52800, 91200, 86400, 127200],
            '_field': ['dosen', 'dosen', 'dosen', 'dosen', 'dosen'],
            '_measurement': ['vaccine_delivery', 'vaccine_delivery', 'vaccine_delivery', 'vaccine_delivery', 'vaccine_delivery'],
            'line_name': ['astra', 'astra', 'astra', 'astra', 'astra'],
            'region': ['DE-BW', 'DE-BW', 'DE-BW', 'DE-BW', 'DE-BW']
        })
        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_query_states_most_vaccines(self):
        """Test states with most vaccines query
            * compare expected dataframe to result dataframe
        """
        result_df = self.model.read_states_most_vaccines().head()
        result_df = result_df[['y_axis', '_field',
                               '_measurement', 'impfstoff', 'x_axis']]
        result_df['y_axis'] = result_df['y_axis'].astype('int64')
        expected_df = pd.DataFrame({
            'y_axis': [690014, 1000762, 256260, 3040596, 3753009],
            '_field': ['dosen', 'dosen', 'dosen', 'dosen', 'dosen'],
            '_measurement': ['vaccine_delivery', 'vaccine_delivery', 'vaccine_delivery', 'vaccine_delivery', 'vaccine_delivery'],
            'impfstoff': ['moderna', 'johnson', 'moderna', 'moderna', 'moderna'],
            'x_axis': ['DE-BB', 'DE-BE', 'DE-BUND', 'DE-BW', 'DE-BY']
        })
        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_execute_query(self):
        """Test query execution function
            * test with wrong query
            * test with correct query that should return an empty dataframe
        """
        query = "CompletlyWrongQuery"
        result_df = self.model._execute_query(query)
        expected_df = pd.DataFrame()
        pd.testing.assert_frame_equal(result_df, expected_df)

        start = "2020-01-02T00:00:00Z"
        stop = "2020-01-01T00:00:00Z"
        query = f'''from(bucket:"{self.model.bucket}")
                    |> range(start: {start}, stop: {stop})
        '''
        result_df = self.model._execute_query(query)
        expected_df = pd.DataFrame()
        pd.testing.assert_frame_equal(result_df, expected_df)

    def test_delete(self):
        """Test delete function
            * delete some data and create it afterwards again
        """
        result = self.model.delete("vaccine_delivery")
        self.assertEqual(result, True)

        self.model.create_vaccine_deliveries()

    def test_get_data_directory_file(self):
        """Test get data directory file
            * test a function call with a number
            * test a function call with a string
        """
        with self.assertRaises(TypeError):
            self.model._get_data_directory_file(42)

        self.model._get_data_directory_file("HelloWorld")


if __name__ == "__main__":
    unittest.main()

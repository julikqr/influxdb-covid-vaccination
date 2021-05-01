from influxdb_client import InfluxDBClient


class Model:
    def __init__(self, token="my-super-secret-auth-token", org="my-org", bucket="my-bucket", url="http://localhost:8086"):
        # self.client
        self.token = token
        self.bucket = bucket
        self.org = org
        self.dburl = url

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

    def execute_query(self, button):
        return f"Execute {button} query"

from model import Model
from view import View


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self)
        self.dbstatus = False

        self.connect_to_db()
        self.view.start_gui()

    def connect_to_db(self):
        self.dbstatus = self.model.connect_to_db()
        if self.dbstatus:
            print("Succesfully connected to InfluxDB")
            self.view.set_status("Succesfully connected to InfluxDB")
        else:
            self.view.set_status("Connection to InfluxDB failed")
            print("Connection to InfluxDb failed")

    def button_clicked(self, button):
        status = self.model.execute_query(button)
        self.view.set_status(status)

        if self.dbstatus:
            if button == "Create vaccine deliveries":
                self.create_vaccine_deliveries()
            if button == "Read - Germany BW vaccine deliveries":
                self.read_vaccine_deliveries_debw()
            if button == "Delete vaccine deliveries":
                self.model.delete("vaccine_delivery")
        else:
            self.view.set_status("DB COnnection failed")

    def create_vaccine_deliveries(self):
        if self.model.create_vaccine_deliveries():
            self.view.set_status("Vaccine delivery data was written to DB")
        else:
            self.view.set_status("Could not write Vaccine delivery data to DB")

    def read_vaccine_deliveries_debw(self):
        result_df = self.model.read_vaccine_deliveries_debw()
        if result_df.size == 0:
            self.view.set_status("Read Germany BW vaccine deliveries failed")
        else:
            self.view.set_status("Read Germany BW vaccine deliveries")
            self.view.plot_df(result_df)
        # print(tables.head())
        # print(tables.size)
        # self.view.plot_pandas("plot")
        # for table in tables:
        #    print()
        #    for record in table.records:
        #        print(
        #            f'Time: {record.values["_time"]}; region: {record.values["region"]}; impfstoff: {record.values["impfstoff"]}; Dosen: {record.values["_value"]}')

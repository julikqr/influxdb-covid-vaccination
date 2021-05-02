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
            self.view.set_status("Succesfully connected to InfluxDB")
        else:
            self.view.set_status(
                "Connection failed - Press any button to connect")

    def button_clicked(self, button):
        if self.dbstatus:
            if button == "Create vaccine deliveries":
                self.create_vaccine_deliveries()
            if button == "Read - Germany BW vaccine deliveries":
                self.read_vaccine_deliveries_debw()
            if button == "Delete vaccine deliveries":
                self.delete_vaccine_deliveries()
            if button == "Read - German states with most vaccines":
                self.read_states_most_vaccines()
        else:
            self.connect_to_db()

    def create_vaccine_deliveries(self):
        if self.model.create_vaccine_deliveries():
            self.view.set_status("DB is filled with vaccine delivery data")
        else:
            self.view.set_status("Could not write Vaccine delivery data to DB")

    def read_vaccine_deliveries_debw(self):
        result_df = self.model.read_vaccine_deliveries_debw()
        if result_df.size == 0:
            self.view.set_status("Please create data first")
        else:
            self.view.set_status("Read Germany BW vaccine deliveries")
            self.view.plot_df(
                result_df, "Germany Baden-Wuerttemberg vaccine deliveries", "vaccines")

    def read_states_most_vaccines(self):
        result_dict = self.model.read_states_most_vaccines()
        if len(result_dict) == 0:
            self.view.set_status("Please create data first")
        else:
            self.view.set_status("Read states with most vaccines")
            self.view.plot_result(result_dict)

    def delete_vaccine_deliveries(self):
        if(self.model.delete("vaccine_delivery")):
            self.view.set_status("Vaccine deliveries deleted")
        else:
            self.view.set_status("Failed to delete vaccine deliveries")

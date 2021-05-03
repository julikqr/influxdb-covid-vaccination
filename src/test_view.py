import unittest
from controller import Controller
from view import View
import pandas as pd


class TestCalc(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # runs once before first start
        cls.controller = Controller(start_gui=False)
        cls.view = View(cls.controller)

    def test_create_buttons(self):
        self.view._category_button_names = [
            "Create - vaccine deliveries",
            "Read - Germany BW vaccine deliveries"
        ]
        self.view._create_buttons()

        with self.assertRaises(TypeError):
            self.view._category_button_names = [
                "Create - vaccine deliveries",
                "Read - Germany BW vaccine deliveries",
                1242131
            ]
            self.view._create_buttons()

    def test_plot_line_chart(self):
        test_data = pd.DataFrame({
            'y_axis': [48000, 52800, 91200, 86400, 127200],
            '_field': ['dosen', 'dosen', 'dosen', 'dosen', 'dosen'],
            '_measurement': ['vaccine_delivery', 'vaccine_delivery', 'vaccine_delivery', 'vaccine_delivery', 'vaccine_delivery'],
            'line_name': ['astra', 'astra', 'astra', 'astra', 'astra'],
            'region': ['DE-BW', 'DE-BW', 'DE-BW', 'DE-BW', 'DE-BW'],
            'x_axis': ['2021-02-06T00:00:00Z', '2021-02-08T00:00:00Z', '2021-02-12T00:00:00Z', '2021-02-16T00:00:00Z', '2021-02-20T00:00:00Z']
        })
        self.view.plot_line_chart(
            test_data, "x_label", "y_label", "title", plot=False)

        test_data = 0
        with self.assertRaises(AttributeError):
            self.view.plot_line_chart(
                test_data, "x_label", "y_label", "title", plot=False)

        with self.assertRaises(TypeError):
            self.view.plot_line_chart()

    def test_plot_bar_chart(self):
        test_data = pd.DataFrame({
            'y_axis': [690014, 1000762, 256260, 3040596, 3753009],
            '_field': ['dosen', 'dosen', 'dosen', 'dosen', 'dosen'],
            '_measurement': ['vaccine_delivery', 'vaccine_delivery', 'vaccine_delivery', 'vaccine_delivery', 'vaccine_delivery'],
            'impfstoff': ['moderna', 'johnson', 'moderna', 'moderna', 'moderna'],
            'x_axis': ['DE-BB', 'DE-BE', 'DE-BUND', 'DE-BW', 'DE-BY']
        })
        self.view.plot_bar_chart(test_data, "x_label",
                                 "y_label", "title", plot=False)

        test_data = 0
        with self.assertRaises(AttributeError):
            self.view.plot_bar_chart(
                test_data, "x_label", "y_label", "title", plot=False)

        with self.assertRaises(TypeError):
            self.view.plot_bar_chart()


if __name__ == "__main__":
    unittest.main()

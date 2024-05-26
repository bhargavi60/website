import json
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

class Base_Booking_Manager(ABC):
    def __init__(self, site_data):
        #self.config_file = config_file
        self.site_data =site_data
        #self.load_data()
        self.load_data2()

    '''def load_data(self):
        try:
            with (open(self.config_file, "r") as f):
                config_data = json.load(f)
                params_file = config_data.get("params_file")
                if params_file:
                    with open(params_file, "r") as params_file:
                        self.site_data = json.load(params_file)
                        print("Loaded site data:", self.site_data)
                else:
                    print("No params file found in the config data")
        except FileNotFoundError:
            print("Error: File not found.")
        except json.JSONDecodeError:
            print("Error: Unable to decode JSON data.")
        except Exception as e:
            print("Error:", e)
    '''
    def load_data2(self):
        try:
            '''with open(self.config_file, "r") as f:
                config_data = json.load(f)
                params_file = config_data.get("params_file")
                if params_file:
                    with open(params_file, "r") as params_f:
                        self.site_data = json.load(params_f) 
            '''
            site_name = self.site_data.get("name")
            if site_name == "VU":
                payload_file = "voordeluitjes_payload.json"
            elif site_name == "TD":
                payload_file = "traveldeal_payload.json"
            else:
                print("Error: Invalid site name")

            try:
                with open(payload_file, "r") as payload_f:
                    self.data = json.load(payload_f)
            except FileNotFoundError:
                print(f"Error: {payload_file} not found.")
            except json.JSONDecodeError:
                print(f"Error: Unable to decode JSON data from {payload_file}.")
            except Exception as e:
                print("Error:", e)

        except FileNotFoundError:
            print("Error: File not found.")
        except json.JSONDecodeError:
            print("Error: Unable to decode JSON data.")
        except Exception as e:
            print("Error:", e)


    def increment_date(self, date_str, duration):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return (date_obj + timedelta(days=duration)).strftime("%Y-%m-%d")

    def get_date_range(self, start_date_str, end_date_str):
        start_date_str = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date_str = datetime.strptime(end_date_str, "%Y-%m-%d")

        current_date = start_date_str
        date_range = []

        while current_date <= end_date_str:
            date_range.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)

        return date_range

    @abstractmethod
    def  get_total_price(self, data):
        pass

    @abstractmethod
    def run_bookings(self, outputFile):
        pass
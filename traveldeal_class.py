import csv
import time
import requests
from datetime import datetime, timedelta
from base_class import Base_Booking_Manager
from request_file import ApiClient

class BookingManager2(Base_Booking_Manager):

    def __init__(self,  site_data):
        super().__init__( site_data)
        self.data = None
    def get_total_price(self, data):
        api_client = ApiClient(data.get("base_url"), data.get("url_2"))
        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = api_client.post(url=data.get("url_2"), data=data, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                #print("Response td:", response_data)
                total_price = response_data.get("data", {}).get("createReceipt", {}).get("totalWithSurcharges", {}).get("amount")
                return total_price

            else:
                if response.status_code == 500:
                    response_data = response.json()
                    print("Response td:", response)
                    total_price = 0
                    return total_price
                else:
                    print("error occured")
        except Exception as e:
            print(f"An exception occurred: {e}")


    def run_bookings(self, outputFile):
        #self.load_data()
        self.load_data2()
        data = self.data
        site_data = self.site_data

        print(self.data)
        print(self.site_data)

        if not data or not site_data:
            print("Error: Data not loaded correctly.")
            return

        #csv_file = "response_data0.csv"
        self.fieldnames = [
            "room_id", "arrivalDate", "totalPrice"
        ]

        with open(outputFile, "w", newline="") as csvfile:

            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()

            site = site_data
            #for site in site_data["site"]:
            if site.get("name") == "TD":
                base_url = site.get("base_url")
                url_2 = site.get("url_2")
                #base_url = site.get("site", [{}])[1].get("base_url")
                print(base_url)
                #url_2 = site_data("site", [{}])[1].get("url_2")
                '''rooms = site_data("site", [{}])[1].get("rooms")
                start_date = site_data("site", [{}])[1].get("variables", {}).get("date")
                end_date = site_data("site", [{}])[1].get("variables", {}).get("end_date")'''
                rooms = site.get("rooms", [])
                start_date = site.get("variables", {}).get("date")
                end_date = site.get("variables", {}).get("end_date")
                print(start_date)
                print(end_date)

                current_date = start_date
                while current_date <= end_date:
                    for room in rooms:
                        room_id = room.get("id")
                        data_copy = data.copy()
                        #room_id= site.get("rooms", [{}]).get("id")
                        #data_copy["roomId"] = room_id
                        #current_date = site.get("variables", {}).get("date")
                        data_copy["variables"]["rooms"][0]["id"] = room_id
                        data_copy["variables"]["date"] = current_date

                        total_price = self.get_total_price(data_copy)
                        print(total_price)
                        if total_price is not None:
                            writer.writerow({
                                "room_id": room_id,
                                "arrivalDate": current_date,
                                "totalPrice": total_price / 100
                            })
                            print("Data written to CSV")
                            print(
                                f"Data stored for Room={room_id}, ArrivalDate={current_date}, TotalPrice={total_price / 100}")

                        else:
                            print(
                                f"Data stored for Room={room_id}, ArrivalDate={current_date}, TotalPrice={0}")
                        time.sleep(0.5)


                    current_date = (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(days=1)).strftime(
                        "%Y-%m-%d")

                start_date = current_date


        print("Data stored in", outputFile)
        csvfile.close()


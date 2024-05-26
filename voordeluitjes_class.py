import csv
import time
import copy
import json
import requests
from datetime import datetime, timedelta
from base_class import Base_Booking_Manager
from request_file import ApiClient

class BookingManager(Base_Booking_Manager):
    def __init__(self, site_data):
        super().__init__( site_data)
        #self.data = None
    def get_total_price(self, data):
        api_client = ApiClient(data.get("base_url"), data.get("url_2"))
        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = api_client.post(url=data.get("url_2"), data=data, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                print("Response vu:", response)
                total_price = response_data.get("totalPrice")
                print(
                    f"Data stored for: Location={data.get('locationId')}, Hotel={data.get('hotel_name')}, Package={data.get('packageId')}, Accommodation={data.get('accommodations')[0].get('name')}, ArrivalDate={data.get('arrivalDate')}, TotalPrice={total_price}")
                return total_price
            else:
                print(f"Error occurred for request: {data}")
        except Exception as e:
            print(f"An exception occurred: {e}")
        return None
    def run_bookings(self, outputFile):
        #self.load_data()
        #self.load_data2()
        data = self.data
        site_data = self.site_data

        if not data or not site_data:
            print("Error: Data load kale vu runbookings lo chodu")
            return
        #csv_file = "response_data0.csv"

        self.fieldnames = [
            "locationId", "hotel_name", "packageId", "accommodationId",
            "accommodationName", "arrivalDate", "totalPrice"
        ]

        with open(outputFile, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()

            site = site_data
            for site in site_data.get("site", []):
                base_url = site.get("base_url")
                if site.get("name") == "VU":
                    #base_url = site.get("base_url")
                    url_2 = site.get("url_2")
                    start_date_str = site.get("arrivalDate")
                    end_date_str = site.get("end_date")
                    print(start_date_str)
                    print(end_date_str)


                    locations = site.get("location", [])
                    #print(data)
                    print(site_data)
                    #data_copy = data.copy()

                    for location in locations:
                        location_id = location.get("locationId")
                        print(location_id)
                        hotel_name = location.get("hotel_name")
                        #url_2 = location.get("url_2")
                        packages = location.get("package", [])

                        for package in packages:
                            package_id = package.get("packageId")
                            extras_id = package.get("extras", {}).get("id")
                            #data_copy = copy.deepcopy(site_data)
                            #data_copy["packageId"] = package_id
                            print(package_id)
                            package_accommodations = package.get("accommodations", [])

                            iCounter = 0
                            for accommodation in package_accommodations:
                                accommodation_id = accommodation.get("id")
                                accommodation_name = accommodation.get("name")

                                data_copy = copy.deepcopy(data)
                                print(data)

                                # accommodation_id = site.get("accommodations", [{}])[0].get("id")
                                # accommodation_name = site.get("accommodations", [{}])[0].get("name")

                                data_copy["accommodations"][0]["id"] = accommodation_id
                                data_copy["accommodations"][0]["name"] = accommodation_name


                                #data_copy["accommodations"][iCounter]["id"] = accommodation_id
                                #data_copy["accommodations"][iCounter]["name"] = accommodation_name
                                print(accommodation_name)
                                #iCounter += 1;

                                date_range = self.get_date_range(start_date_str, end_date_str)

                                for arrival_date_str in date_range:
                                    data_copy = copy.deepcopy(data)
                                    data_copy["arrivalDate"] = arrival_date_str
                                    data_copy["extras"] = [{"id": extras_id}] if extras_id is not None else []


                                    tot_price = self.get_total_price(data_copy)
                                    print(data_copy)

                                    if tot_price is not None:
                                        writer.writerow({
                                            "locationId": location_id,
                                            "hotel_name": hotel_name,
                                            "packageId": package_id,
                                            "accommodationId": accommodation_id,
                                            "accommodationName": accommodation_name,
                                            "arrivalDate": arrival_date_str,
                                            "totalPrice": tot_price
                                        })
                                    time.sleep(0.5)
                    print("data stored in", outputFile)


        '''with open(outputFile, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()

            site = site_data

            for site in site.get("site", []):
                base_url = site.get("base_url")
                if site.get("name") == "VU":
                    base_url = site.get("base_url")
                    url_2 = site.get("url_2")
                    start_date_str = site.get("arrivalDate")
                    end_date_str = site.get("end_Date")
                    print(start_date_str)
                    print(end_date_str)

                locations = site.get("location", [])
                data_copy = data.copy()

                for location in locations:
                    location_id = location.get("locationId")
                    hotel_name = location.get("hotel_name")
                    url_2 = location.get("url_2")
                    packages = location.get("package", [])
                    print(location_id)

                    for package in packages:
                        package_id = package.get("packageId")
                        extras_id = package.get("extras", {}).get("id")
                        data_copy = copy.deepcopy(data)
                        data_copy["packageId"] = package_id
                        package_accommodations = package.get("accomodations", [])
                        print(package_id)

                        for accommodation in package_accommodations:
                            accommodation_id = accommodation.get("id")
                            accommodation_name = accommodation.get("name")
                            #data_copy["accommodations"][0]["id"] = accommodation_id
                            #data_copy["accommodations"][0]["name"] = accommodation_name
                            accommodation_id = accommodation.get("id")
                            accommodation_name = accommodation.get("name")

                            date_range = self.get_date_range(start_date_str, end_date_str)

                            for arrival_date_str in date_range:
                                data_copy["arrivalDate"] = arrival_date_str

                                if extras_id is not None:
                                    data_copy["extras"] = [{"id": extras_id}]

                                tot_Price = self.get_total_price(data_copy)

                                writer.writerow({
                                    "locationId": location_id,
                                    "hotel_name": hotel_name,
                                    "packageId": package_id,
                                    "accommodationId": accommodation_id,
                                    "accommodationName": accommodation_name,
                                    "arrivalDate": arrival_date_str,
                                    "totalPrice": tot_Price
                                })
                                time.sleep(0.5)'''
        print("Data stored in", outputFile)
        print("data rale em rale")
        csvfile.close()
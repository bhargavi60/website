
'''
params.json--config file____rate_scan_config.json

common files in folder request,params,base class _____common_files
loop in main for bboking manager


'''

import json
from voordeluitjes_class import BookingManager
from traveldeal_class import BookingManager2

'''paramsFile: any = ""
outputFile: any = ""
'''
def load_Config_File(config_file):
    try:
        with open(config_file, "r") as f:
            config_data = json.load(f)
            return config_data.get("params_file")
            #paramsFile = config_data.get("params_file")
            #outputFile = config_data.get("Output File")
    except FileNotFoundError:
        print("Error: Config file not found.")
    except json.JSONDecodeError:
        print("Error: Unable to decode JSON data.")
    except Exception as e:
        print("Error:", e)
    #return None

def main():
    config_file = "rate_scan_config.json"
    outputFile = "response_data0.csv"
    paramsFile = load_Config_File(config_file)

    if paramsFile :
        with open(paramsFile, "r") as f:
            data = json.load(f)

        '''for site in data["site"]:
            if site.get("name") == "VU":
                booking_manager = BookingManager(site)
                booking_manager.run_bookings()

            elif site.get("name") == "TD":
                booking_manager2 = BookingManager2(site)
                booking_manager2.run_bookings()
            else:
                print(f"Unsupported site name: {site.get('name')}")
        '''
        booking_manager = ""
        for site in data["site"]:
            if site.get("name") == "VU":
                booking_manager = BookingManager(site)
            elif site.get("name") == "TD":
                booking_manager = BookingManager2(site)
            else:
                print(f"Unsupported site name: {site.get('name')}")
            booking_manager.run_bookings(outputFile)

if __name__ == "__main__":
    main()

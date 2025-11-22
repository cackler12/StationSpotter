import requests
import configparser
import logging
import os
from datetime import datetime
from utils import timezone_map

def convert_and_adjust_time(utc_timestamp: int, observer_timezone: str):
    adjusted_time = utc_timestamp + timezone_map.get(observer_timezone)
    return datetime.fromtimestamp(adjusted_time)

def main():
    logger = logging.getLogger("main")

    config = configparser.ConfigParser()
    config.read('config.ini')
    if (config.sections() != ['LOCATION', 'API_KEY']):
        logger.error("Config file has been corrupted, generating a new config :)")
        if os.path.exists('config.ini'):
            os.rename('config.ini', 'config.OLD')
        config = None
        config = configparser.ConfigParser()
        config['LOCATION'] = {'lattitude': 0.0, 'longitude': 0.0, 'altitude': 0.0}
        config['API_KEY'] = {'key': "INSERT_N2Y0_API_KEY"}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    observer_lattitude = config['LOCATION'].get('lattitude')
    observer_longitude = config['LOCATION'].get('longitude')
    observer_altitude = config['LOCATION'].get('altitude')
    observer_timezone = config['LOCATION'].get('timezone')
    user_api_key = config['API_KEY'].get('key')

    response = requests.get("https://api.n2yo.com/rest/v1/satellite/visualpasses/25544/" + observer_lattitude + "/" + observer_longitude + "/" + observer_altitude + "/1/300/&apiKey=" + user_api_key + "")
    data = response.json()
    if (data.get('error') != None):
        logger.error("Error receiving API response, printing error")
        print(data)
    else:
        if (response.status_code == 200):
            print("Received API Response!")

        for observable_moment in data.get('passes'):
            start_datetime = convert_and_adjust_time(observable_moment.get('startUTC'), observer_timezone)
            max_datetime = convert_and_adjust_time(observable_moment.get('maxUTC'), observer_timezone)
            end_datetime = convert_and_adjust_time(observable_moment.get('endUTC'), observer_timezone)
            print("You can start seeing the ISS if you look " + observable_moment.get("startAzCompass") + " at " + str(start_datetime))
            print("You can see the ISS at its highest point if you look " + observable_moment.get('maxAzCompass') + " at " + str(max_datetime))
            print("The ISS will exit your local sky heading " + observable_moment.get('endAzCompass') + " at " + str(end_datetime))

    


if __name__ == "__main__":
    main()
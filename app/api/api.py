import os
import requests

class ElectricityAPI:
    def __init__(self):
        self.api_key = os.getenv('ELECTRICITY_MAPS_API_KEY')
        self.headers = {'auth-token': self.api_key}
        self.url = 'https://api.electricitymap.org/'

    def get_carbon_intensity_api(self, endpoint):
        api_get = requests.get(self.url+endpoint, headers=self.headers)
        if api_get.status_code == 404:
            print ("Data not found for this country")
            return None
        else:
            return api_get.json()['carbonIntensity']

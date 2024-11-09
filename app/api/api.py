import os
import requests

class ElectricityAPI():
    def __init__(self):
        self.api_key = os.getenv('ELECTRICITY_MAPS_API_KEY')
        self.headers = {'auth-token': self.api_key}
        self.url = 'https://api.electricitymap.org/'

    def test_api_endpoint(self, endpoint):
        print(self.url+endpoint)
        api_get = requests.get(self.url+endpoint, headers=self.headers)
        print(f"API GET in {endpoint} returned: {api_get}")
        print(api_get.content)

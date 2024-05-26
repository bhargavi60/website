import requests
import json
from urllib.parse import urljoin
class ApiClient:
    def __init__(self, base_url, endpoint):
        self.base_url = base_url
        self.endpoint = endpoint

    def _make_request(self, method, url, data=None, headers=None, auth=None):
        url = urljoin(self.base_url, self.endpoint)

        if data is not None:
            data = json.dumps(data)

        response = requests.request(method, url, data=data, headers=headers, auth=auth)
        if response.status_code != 200:
             print("Error occured", response)
        return response

    def post(self, url, data=None, headers=None, auth=None):
        return self._make_request('POST', url, data=data, headers=headers, auth=auth)

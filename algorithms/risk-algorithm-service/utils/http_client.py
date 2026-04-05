import requests
from typing import Dict, Any, Optional


class HttpClient:
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.session = requests.Session()

    def post(self, url: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> requests.Response:
        return self.session.post(url, data=data, json=json, timeout=self.timeout)

    def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        return self.session.get(url, params=params, timeout=self.timeout)

    def close(self):
        self.session.close()


http_client = HttpClient()
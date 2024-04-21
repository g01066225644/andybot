import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class Requests:
    @staticmethod
    def session(url, params=None):
        return Requests.hidden_session().get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                                         'Chrome/122.0.0.0 Safari/537.36'},
                                             params=params)

    @staticmethod
    def hidden_session(retries=5, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None, ):
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

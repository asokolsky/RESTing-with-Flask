from requests import Session
from urllib.parse import urljoin
from typing import Any, Tuple


class rest_client:
    '''
    REST client can use requests.request or requests.Session.
    I prefer the second option because:
    it allows to make multiple requests over the same pair of the connected
    sockets. Not only it is more efficient but also allows to carry
    authentication information. No that this is important.  At least not yet.
    '''

    def __init__(self, iface: str, port: int, verbose: bool) -> None:
        '''
        In: iface - server interface, or host name
            sport - server port
        '''
        self.base_url = f'http://{iface}:{port}'
        self.verbose = verbose
        self.ses = Session()
        return

    def get(self, uri: str) -> Tuple[int, Any]:
        '''
        Issue HTTP GET to base_url + uri
        returns (http_status, response_json)
        Throws requests.exceptions.ConnectionError when connection fails
        '''
        url = urljoin(self.base_url, uri)
        if self.verbose:
            print('HTTP GET', url, '...')
        resp = self.ses.get(url)
        if self.verbose:
            print('HTTP GET', url, '=>', resp.status_code, ',',
                  str(resp.json()))
        return (resp.status_code, resp.json())

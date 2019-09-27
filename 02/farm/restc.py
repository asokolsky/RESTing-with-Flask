from requests import Session
from urllib.parse import urljoin

class rest_client:
    '''
    HTTP client can use requests.request or requests.Session.
    I prefer the second option because:
    it allows to make multiple requests over the same pair of the connected
    sockets. Not only it is more efficient but also allows to carry
    authentication information. No that this is important.  At least not yet.
    '''

    def __init__(self, siface, sport, verbose):
        '''
        In:
        siface - server interface, or host name
        sport - server port
        '''
        self.base_url = 'http://' + siface + ':' + str(sport)
        self.verbose = verbose
        self.ses = Session()
        return

    def get(self, uri):
        '''
        Issue HTTP GET to a base_url + uri
        returns (http_status, response_json)
        Throws requests.exceptions.ConnectionError when connection fails
        '''
        url = urljoin(self.base_url, uri)
        if self.verbose:
            print('HTTP GET', url, '...')
        resp = self.ses.get(url)
        if self.verbose:
            print('HTTP GET =>', resp.status_code, ',', str(resp.json()))
        return (resp.status_code, resp.json())

    def post(self, uri, pdata):
        '''
        Issue HTTP POST to a base_url + uri
        returns (http_status, response_json)
        Throws requests.exceptions.ConnectionError when connection fails
        '''
        url = urljoin(self.base_url, uri)
        if self.verbose:
            print('HTTP POST', url, str(pdata))
        resp = self.ses.post(url, json=pdata)
        if self.verbose:
            print('HTTP POST =>', resp.status_code, ',', str(resp.json()))
        return (resp.status_code, resp.json())

    def delete(self, uri):
        '''
        Issue HTTP DELETE to a base_url + uri
        returns (http_status, response_json)
        Throws requests.exceptions.ConnectionError when connection fails
        '''
        url = urljoin(self.base_url, uri)
        if self.verbose:
            print('HTTP DELETE', url, '...')
        resp = self.ses.delete(url)
        if self.verbose:
            print('HTTP DELETE =>', resp.status_code, ',', str(resp.json()))
        return (resp.status_code, resp.json())

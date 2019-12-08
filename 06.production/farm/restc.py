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

    def __init__(self, siface, sport, verbose, dumpHeaders):
        '''
        In:
        siface - server interface, or host name
        sport - server port
        '''
        self.base_url = 'http://' + siface + ':' + str(sport)
        self.verbose = verbose
        self.dumpHeaders = dumpHeaders
        self.ses = Session()
        return

    def close(self):
        '''
        Close the underlying TCP connection
        '''
        self.ses.close()
        return

    def print_req(self, method, url, data):
        if not self.verbose:
            return
        if data is None:
            data = ''
        print('HTTP', method, url, data, '...')
        return

    def print_resp(self, method, resp):
        if self.verbose:
            print('HTTP', method, '=>', resp.status_code, ',', str(resp.json()))
        if self.dumpHeaders:
            print('HTTP Response Headers:')
            for h in resp.headers:
                print('   ', h, ':', resp.headers[h])
        return

    def get(self, uri):
        '''
        Issue HTTP GET to a base_url + uri
        returns (http_status, response_json)
        Throws requests.exceptions.ConnectionError when connection fails
        '''
        url = urljoin(self.base_url, uri)
        self.print_req('GET', url, None)
        resp = self.ses.get(url)
        self.print_resp('GET', resp)
        return (resp.status_code, resp.json())

    def post(self, uri, pdata):
        '''
        Issue HTTP POST to a base_url + uri
        returns (http_status, response_json)
        Throws requests.exceptions.ConnectionError when connection fails
        '''
        url = urljoin(self.base_url, uri)
        self.print_req('POST', url, pdata)
        resp = self.ses.post(url, json=pdata)
        self.print_resp('POST', resp)
        return (resp.status_code, resp.json())

    def delete(self, uri):
        '''
        Issue HTTP DELETE to a base_url + uri
        returns (http_status, response_json)
        Throws requests.exceptions.ConnectionError when connection fails
        '''
        url = urljoin(self.base_url, uri)
        self.print_req('DELETE', url, None)
        resp = self.ses.delete(url)
        self.print_resp('DELETE', resp)
        return (resp.status_code, resp.json())

    def put(self, uri, pdata):
        '''
        Issue HTTP PUT to a base_url + uri
        returns (http_status, response_json)
        Throws requests.exceptions.ConnectionError when connection fails
        '''
        url = urljoin(self.base_url, uri)
        self.print_req('PUT', url, pdata)
        resp = self.ses.put(url, json=pdata)
        self.print_resp('PUT', resp)
        return (resp.status_code, resp.json())

    def patch(self, uri, pdata):
        '''
        Issue HTTP PATCH to a base_url + uri
        returns (http_status, response_json)
        Throws requests.exceptions.ConnectionError when connection fails
        '''
        url = urljoin(self.base_url, uri)
        self.print_req('PATCH', url, pdata)
        resp = self.ses.patch(url, json=pdata)
        self.print_resp('PATCH', resp)
        return (resp.status_code, resp.json())

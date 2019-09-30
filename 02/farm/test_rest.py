#
# HTTP Client Test
#
# Launch it by issuing:
#  python3 -m unittest test_restc -v
#

import unittest
import restc

class TestRestC(unittest.TestCase):
    '''
    Test HTTP client
    '''

    def setUp(self):
        '''
        Executed prior to each test.
        '''
        iface = 'httpbin.org'
        port = 80
        verbose = True
        self.cl = restc.rest_client(iface, port, verbose)
        
        return

    def tearDown(self):
        '''
        executed after each test
        '''

        return

    def test_get(self):
        '''
        rest_client.get test
        '''


        return

    def test_post(self):
        '''
        rest_client.post test
        '''

        return

    def test_delete(self):
        '''
        rest_client.delete test
        '''
        
        return


if __name__ == '__main__':
    unittest.main()
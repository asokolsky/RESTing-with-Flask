#
# Farm Testing
#
# Launch it by issuing:
#  python3 -m unittest test_farm -v
#

import unittest
from uuid import uuid4 

from app import app, create_app, init_app

class TestFarm(unittest.TestCase):

    def setUp(self):
        '''
        Executed prior to each test.
        Launch Farm server - compare to farm::farm_start
        '''
        app = create_app('farm.cfg')
        init_app(app)

        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)
        return

    def tearDown(self):
        '''
        executed after each test
        '''
        return

    def get(self, uri):
        '''
        Wrapper around get
        '''
        # , follow_redirects=True
        return self.app.get('/api/v1/' + uri)

    def post(self, uri, jdata):
        '''
        Wrapper around post
        '''
        return self.app.post('/api/v1/' + uri, json=jdata)


    def test_animals(self):
        '''
        Verify functionality fo the animal collection
        '''
        uri = 'animal'
        resp = self.get(uri)
        self.assertEqual(resp.status_code, 200)
        #rd = resp.json()

        id = str(uuid4())
        ad = {
            'id' : id,
            'weight' : 4500,
            'nick' : 'fluff'
        }
        resp = self.post(uri, ad)
        self.assertEqual(resp.status_code, 201)
        return

if __name__ == '__main__':
    unittest.main()

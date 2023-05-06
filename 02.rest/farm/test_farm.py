#
# Farm Testing
#
# To launch it:
#  Farm does NOT have to run!
#  In a terminal start the automated test against the farm:
#  alex@latitude:~/Projects/RESTing-with-Flask/02/farm$ python3 test_farm.py
#

import unittest
from uuid import uuid4
from json import loads

from app import create_app, init_app


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
        #
        # This is important!
        # we will be using a test FLASK client
        # which does not required for the flask app to run!
        #
        app.testing = True
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

    def delete(self, uri):
        '''
        Wrapper around delete
        '''
        return self.app.delete('/api/v1/' + uri)

    def post_an_animal(self):
        '''
        Post a single animal to the collection
        '''
        uri = 'animal'
        id = str(uuid4())
        ad = {
            'id': id,
            'weight': 4500,
        }
        return self.post(uri, ad)

    def delete_an_animal(self, id):
        return self.delete('animal/' + id)

    def get_animals(self):
        uri = 'animal'
        resp = self.get(uri)
        self.assertEqual(resp.status_code, 200)
        # return resp.get_data()
        # return resp.json()
        return loads(resp.get_data(as_text=True))

    def test_animals(self):
        '''
        Verify functionality fo the animal collection
        '''

        # any animals out there?
        ans = self.get_animals()
        self.assertEqual(ans, [])

        iAnimals = 5
        for i in range(iAnimals):
            self.post_an_animal()

        # verify animals were created
        ans = self.get_animals()
        self.assertEqual(len(ans), iAnimals)

        # delete just one
        an = ans[iAnimals // 2]
        id = an['id']
        resp = self.delete_an_animal(id)
        self.assertEqual(resp.status_code, 200)

        # try to delete the animal again
        resp = self.delete_an_animal(id)
        self.assertEqual(resp.status_code, 404)

        # verify there is one less animal
        ans = self.get_animals()
        self.assertEqual(len(ans), iAnimals - 1)
        return


if __name__ == '__main__':
    unittest.main()

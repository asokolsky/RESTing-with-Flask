#
# Farm Testing
#
# To launch it:
#  Farm does NOT have to run!
#  In a terminal start the automated test against the farm:
#  alex@latitude:~/Projects/RESTing-with-Flask/02/farm$ python3 test_farm.py
#

import unittest
import random
from uuid import uuid4 
from json import loads

from app import app, create_app, init_app

def get_random(ar):
    return ar[random.randint(0, len(ar)-1)]

class TestFarm(unittest.TestCase):

    def setUp(self):
        '''
        Executed prior to each test.
        Launch Farm server - compare to farm::farm_start
        '''
        random.seed()

        app = create_app('farm_test.cfg')
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
        res = self.app.post('/api/v1/' + uri, json=jdata)
        print('res', res)
        return res

    def delete(self, uri):
        '''
        Wrapper around delete
        '''
        return self.app.delete('/api/v1/' + uri)

    def new_animal(self):
        '''
        Generate a valid animal record
        '''
        # let's give it a name
        n1 = ['little', 'big', 'tiny', 'baby', 'babe', 'ugly', 'pretty',
              'skinny', 'lady', 'sixfinger', 'handsome', 'proud', 'steady',
              'blond']
        n2 = ['bella', 'coco', 'max', 'buddy', 'daisy', 'lola', 'luna',
              'lucy', 'harley', 'charlie', 'pepper', 'shadow', 'gracie', 'jack',
              'milo', 'rocky', 'sadie', 'stella']
        name = get_random(n1) + ' ' + get_random(n2)
        ad = {
            'id' : str(uuid4()),
            'species': get_random(['chicken', 'cow']),
            'name' : name,
            'sex': get_random(['female', 'male'])
        }
        return ad

    def post_an_animal(self):
        '''
        Post a single animal to the collection
        '''
        return self.post('animal', self.new_animal())

    def delete_an_animal(self, id):
        return self.delete('animal/' + id)

    def get_animals(self):
        uri = 'animal'
        resp = self.get(uri)
        self.assertEqual(resp.status_code, 200)
        #return resp.get_data()
        # return resp.json()
        return loads(resp.get_data(as_text=True))

    def test_animals(self):
        '''
        Verify functionality of the animal collection
        '''

        # any animals out there?
        ans = self.get_animals()
        self.assertEqual(ans, [])

        iAnimals = 59
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

        # verify that schema validation indeed works
        ad = self.new_animal()
        ad['species'] = 'alien'
        resp = self.post('animal', ad)
        self.assertEqual(resp.status_code, 409)

        # verify that schema validation indeed works
        ad = self.new_animal()
        ad['dob'] = '2019-10-20'
        resp = self.post('animal', ad)
        self.assertEqual(resp.status_code, 201)

        # verify that schema validation indeed works
        ad = self.new_animal()
        ad['dob'] = '2019-1-20'
        resp = self.post('animal', ad)
        self.assertEqual(resp.status_code, 409)
        return

if __name__ == '__main__':
    unittest.main()

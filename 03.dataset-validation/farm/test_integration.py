#
# Integration test plan:
#  - Launch server
#  - test serving static content
#  - test making REST API requests
#
import multiprocessing
import random
import restc
import sys
from time import sleep
from typing import Any, List
import unittest
from urllib.parse import urljoin
from uuid import uuid4

from app import create_app, init_app


def get_random(ar: List[Any]) -> Any:
    '''
    Get a random element of the array
    '''
    return ar[random.randint(0, len(ar)-1)]


def farm_start() -> None:
    '''
    Starts and runs flask
    '''

    app = create_app('farm.cfg')
    iface = app.config.get('FARM_IF')
    port = int(str(app.config.get('FARM_PORT')))
    init_app(app)
    try:
        app.run(
            host=iface,
            port=port,
            threaded=True,
            processes=1)

    except KeyboardInterrupt:
        print('Ctrl-C caught in farm start, aborting.', file=sys.stderr)

    except Exception as e:
        print('Failed to start farm: ', str(e))

    return


class TestIntegration(unittest.TestCase):
    '''
    Test cases for testing Flask app
    '''
    # Class members:
    # proc: multiprocessing.Process - farm server
    # restc: restc.rest_client - client

    @classmethod
    def setUpClass(cls):
        '''
        Executed once for module and before any test.
        Launch Farm server.
        '''
        random.seed()

        cls.proc = multiprocessing.Process(target=farm_start)
        cls.proc.start()
        print('Started', cls.proc)

        # from conf/farm.cfg
        iface = '127.0.0.1'
        port = 44444
        verbose = False
        dumpHeaders = False
        cls.restc = restc.rest_client(iface, port, verbose, dumpHeaders)
        #
        # wait until the server is up and running
        #
        url = urljoin(cls.restc.base_url, '/index.html')
        retries = 5
        retry = 0
        while retry < retries:
            # give an opportunity to the server to start
            sleep(.1)
            # get the static content as indication of the server readiness
            print('GET', url)
            try:
                cls.restc.ses.get(url)
                # connection established!
                return

            except Exception:
                pass
            retry += 1

        # failed to establish connection after retries
        return

    @classmethod
    def tearDownClass(cls):
        '''
        Once for all the tests in this module..
        Kill Farm server.
        '''
        cls.restc.close()

        print('Terminating', cls.proc)
        cls.proc.kill()
        cls.proc.join()
        return

    def new_animal(self):
        '''
        Generate a valid animal record
        '''
        # let's give it a name
        n1 = ['little', 'big', 'tiny', 'baby', 'babe', 'ugly', 'pretty',
              'skinny', 'lady', 'sixfinger', 'handsome', 'proud', 'steady',
              'blond']
        n2 = ['bella', 'coco', 'max', 'buddy', 'daisy', 'lola', 'luna', 'lucy',
              'harley', 'charlie', 'pepper', 'shadow', 'gracie', 'jack',
              'milo', 'rocky', 'sadie', 'stella']
        name = get_random(n1) + ' ' + get_random(n2)
        ad = {
            'id': str(uuid4()),
            'species': get_random(['chicken', 'cow']),
            'name': name,
            'sex': get_random(['female', 'male'])
        }
        return ad

    def post_an_animal(self):
        '''
        Post a single animal to the collection
        '''
        return self.restc.post('/api/v1/animal', self.new_animal())

    def delete_an_animal(self, id):
        return self.restc.delete('/api/v1/animal/' + id)

    def get_animals(self):
        uri = '/api/v1/animal'
        status_code, data = self.restc.get(uri)
        self.assertEqual(status_code, 200)
        return data

    def test_static_content(self):
        '''
        Verify that the static content is being served
        '''
        url = urljoin(self.restc.base_url, '/index.html')
        print('GET', url)
        resp = self.restc.ses.get(url)
        self.assertEqual(resp.status_code, 200)
        return

    def test_animals(self):
        '''
        Verify functionality of the animal collection
        '''

        # any animals out there?
        ans = self.get_animals()
        self.assertEqual(ans, [])

        iAnimals = 5
        for i in range(iAnimals):
            status_code, _ = self.post_an_animal()
            self.assertEqual(status_code, 201)

        # verify animals were created
        ans = self.get_animals()
        self.assertEqual(len(ans), iAnimals)

        # delete just one
        an = ans[iAnimals // 2]
        id = an['id']
        status_code, _ = self.delete_an_animal(id)
        self.assertEqual(status_code, 200)

        # try to delete the animal again
        status_code, _ = self.delete_an_animal(id)
        self.assertEqual(status_code, 404)

        # verify there is one less animal
        ans = self.get_animals()
        self.assertEqual(len(ans), iAnimals - 1)

        # verify that schema validation indeed works
        ad = self.new_animal()
        ad['species'] = 'alien'
        status_code, _ = self.restc.post('/api/v1/animal', ad)
        self.assertEqual(status_code, 409)

        # verify that schema validation indeed works
        ad = self.new_animal()
        ad['dob'] = '2019-10-20'
        status_code, _ = self.restc.post('/api/v1/animal', ad)
        self.assertEqual(status_code, 201)

        # verify that schema validation indeed works
        ad = self.new_animal()
        ad['dob'] = '2019-1-20'
        status_code, _ = self.restc.post('/api/v1/animal', ad)
        self.assertEqual(status_code, 409)
        return


if __name__ == '__main__':
    unittest.main()

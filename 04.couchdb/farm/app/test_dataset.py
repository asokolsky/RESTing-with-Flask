#
# Testing DataSet
#
# Launch it by issuing:
#  python3 -m unittest test_dataset -v
#
import random
# import os
# import sys
from schema import Schema
import unittest

from .dataset import DataSetRAM

from . import create_app, init_app
# sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# create benign Schema
NoSchema = Schema(object)


class TestDataset(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        '''
        Executed once for module and before any test.
        Launch Farm server - compare to farm::farm_start
        '''
        random.seed()

        global app
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
        cls.app = app.test_client()
        assert not app.debug
        return

    @classmethod
    def tearDownClass(cls):
        '''
        Once for all the tests in this module..
        '''
        global app
        app = None
        return

    def setUp(self):
        '''
        Executed prior to each test.
        '''
        self.ds = DataSetRAM('test', NoSchema)
        return

    def tearDown(self):
        '''
        executed after each test
        '''
        return

    def test_dataset(self):
        '''
        Verify dataset functionality
        '''
        self.assertEqual(len(self.ds.data), 0)

        key = "1"
        d = {"a": "b"}

        self.assertTrue(self.ds.put(key, d))

        self.assertEqual(len(self.ds.data), 1)

        r = self.ds.get(key)
        self.assertEqual(r, d)

        r = self.ds.pop(key)
        self.assertEqual(r, d)

        self.assertEqual(len(self.ds.data), 0)

        r = self.ds.pop(key)
        self.assertEqual(r, None)
        return


if __name__ == '__main__':
    unittest.main()

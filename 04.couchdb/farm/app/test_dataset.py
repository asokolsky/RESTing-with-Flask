#
# Testing DataSet
#
# Launch it by issuing:
#  python3 -m unittest test_dataset -v
#
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import unittest
from schema import (
    Schema,
    #SchemaError,
    #Use,
)
from dataset import DataSetRAM

from . import app, log, create_app

# create benign Schema
NoSchema = Schema(object)

class TestDataset(unittest.TestCase):

    @classmethod
    def setUpClass( cls ):
        '''
        Once for all the tests in this module..
        '''
        # create log object needed in dataset
        global app
        app = create_app( 'farm.cfg' )
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
        d = {"a":"b"}

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

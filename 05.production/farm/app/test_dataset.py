#
# Testing DataSet
#
# Launch it by issuing:
#  python3 -m unittest test_dataset -v
#

import unittest
from schema import (
    Schema,
    SchemaError,
    Use,
)

from dataset import DataSet

# create benign Schema
NoSchema = Schema(object)

class TestDataset(unittest.TestCase):

    def setUp(self):
        '''
        Executed prior to each test.
        '''
        self.ds = DataSet('test', NoSchema)
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
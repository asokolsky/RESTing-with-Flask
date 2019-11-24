#
# Testing Farm schema
#
# Launch it by issuing:
#  python3 -m unittest test_farm_schema -v
#

import unittest
from schema import (
    #And,
    #Const,
    #Optional,
    #Or,
    #Regex,
    #Schema,
    SchemaError,
    #Use,
)

from farm_schema import (
    AnimalSchema,
    #SchemaEnumError
)

class TestFarmSchema(unittest.TestCase):

    def setUp(self):
        '''
        Executed prior to each test.
        '''
        return

    def tearDown(self):
        '''
        executed after each test
        '''
        return

    def test_animal_schema(self):
        '''
        Verify data validation functionality
        '''

        d = {
            "id": "2b490682-732e-4c30-ba4d-1a99b6d4921d",
            "species": "chicken",
            "sex": "female",
        }
        r = AnimalSchema.validate(d)
        self.assertEqual(r, d)

        # verify optional fields are accepted
        d["name"] = "Al"
        r = AnimalSchema.validate(d)
        self.assertEqual(r, d)

        d["dob"] = "2018-12-31"
        r = AnimalSchema.validate(d)
        self.assertEqual(r, d)

        # negative test cases
        d = {
            "id": "2b490682-732e-4c30-ba4d-1a99b6d4921d",
        }
        with self.assertRaises(SchemaError):
            AnimalSchema.validate(d)

        d = {
            "id": "2b490682-732e-4c30-ba4d-1a99b6d4921d",
            "species": "dinosaur",
            "sex": "female",
        }
        with self.assertRaises(SchemaError):
            AnimalSchema.validate(d)

        d = {
            "id": "2b490682-732e-4c30-ba4d-1a99b6d4921d",
            "species": "chicken",
            "sex": "female",
            "name": ""
        }
        with self.assertRaises(SchemaError):
            AnimalSchema.validate(d)

        d["name"] = "Al"
        d["dob"] = "2019/1/2"
        with self.assertRaises(SchemaError):
            AnimalSchema.validate(d)

        return

if __name__ == '__main__':
    unittest.main()

from schema import And, Optional, Regex, Schema, SchemaError, Use
from typing import Any


#
# Let's first improve on the schema module:
# Need a better support for Enum!
#
class SchemaEnumError(SchemaError):
    '''
    Is thrown when validation of an enum schema fails.
    '''
    pass


class Enum(object):
    '''
    Handler for the enum elements of the schema.
    Belongs in the schema package itself.
    '''
    def __init__(self, *args, **kwargs) -> None:
        '''
        Initialized with valid enum options
        '''
        self.enum_elements = [
            (isinstance(a, str) and a.lower()) or a for a in args]
        return

    def validate(self, data: Any) -> Any:
        '''
        :param data: data to be validated by a provided enum schema.
        :return: returns validated data
        '''
        if isinstance(data, str):
            data = data.lower()
        if data in self.enum_elements:
            return data

        raise SchemaEnumError(f"'{data}' is not one of {self.enum_elements}")


AnimalSchema = Schema({
    'id': str,
    'species': Enum('Chicken', 'Cow'),
    'sex': Enum('Female', 'Male'),
    Optional("name"): And(Use(str), len),
    # YYYY-MM-DD
    Optional("dob"): Regex(r'[0-9]{4}\-[0-1][0-9]\-[0-3][0-9]'),
    # weight in grams? Or rather have it in a time-series db?
    # Optional("weight"): And(Use(int), lambda w: 0 < w <= 10000000),
})

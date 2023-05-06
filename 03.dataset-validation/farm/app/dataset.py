from .farm_schema import AnimalSchema


class DataSet:
    '''
    Class to represent in-memory collection of objects
    '''
    def __init__(self, name, schema):
        '''
        In:
        name - dataset name - e.g. 'animal'
        schema - dataset schema
        '''
        self.name = name
        self.schema = schema
        self.data = dict()
        return

    def get(self, id):
        '''
        Access the record by id
        '''
        return self.data.get(id, None)

    def put(self, id, dat):
        '''
        Stores data into the dataset
        Returns:
            True if dat is validated against schema and is added to the dataset
            False otherwise
        May throw:
            SchemaError
        '''
        if not self.schema.validate(dat):
            return False
        self.data[id] = dat
        return True

    def pop(self, id):
        return self.data.pop(id, None)


# will be storing animals here
theAnimals = DataSet('animal', AnimalSchema)

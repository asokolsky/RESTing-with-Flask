
class DataSet:
    '''
    Class to represent in-memory collection of objects
    '''
    def __init__(self, name):
        '''
        In:
        name - dataset name - e.g. 'animal'
        '''
        self.name = name
        self.data = dict()
        return

    def add(self, id, dat):
        self.data[id] = dat
        return

    def get(self, id):
        '''
        Access the record by id
        '''
        return self.data.get(id, None)

    def put(self, id, dat):
        '''
        Stores data into the dataset
        '''
        self.data[id] = dat
        return

    def pop(self, id):
        return self.data.pop(id, None)


# will be storing animals here
theAnimals = DataSet('animal')

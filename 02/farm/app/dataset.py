
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

# will be storing animals here
theAnimals = DataSet('animal')

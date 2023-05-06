from typing import Any, Dict


class DataSet:
    '''
    Class to represent in-memory collection of objects
    '''
    def __init__(self, name: str) -> None:
        '''
        In:
        name - dataset name - e.g. 'animal'
        '''
        self.name = name
        self.data: Dict[str, Any] = dict()
        return

    def add(self, id: str, dat: Any) -> None:
        self.data[id] = dat
        return

    def get(self, id: str) -> Any:
        '''
        Access the record by id
        '''
        return self.data.get(id, None)

    def put(self, id: str, dat: Any) -> None:
        '''
        Stores data into the dataset
        '''
        self.data[id] = dat
        return

    def pop(self, id: str) -> Any:
        return self.data.pop(id, None)


# will be storing animals here
theAnimals = DataSet('animal')

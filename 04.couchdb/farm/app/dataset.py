from requests import Session
from abc import ABC, abstractmethod 
from farm_schema import AnimalSchema

from . import app, log

class DataSet(ABC):
    '''
    Class to represent collection of objects - in RAM or DB
    Main public APIs are get and put
    '''
    def __init__(self, name, schema):
        '''
        In:
            name - dataset name - e.g. 'animal'
            schema - dataset schema
        '''
        self.name = name
        self.schema = schema
        return

    @abstractmethod
    def get(self, id):
        '''
        Access the record by id
        '''
        pass

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
        
        return self.put_(id, dat)

    @abstractmethod
    def put_(self, id, dat):
        '''
        Stores data into the dataset
        Returns:
            True if dat is validated against schema and is added to the dataset
            False otherwise
        May throw:
            Error
        '''
        pass


class DataSetRAM(DataSet):
    '''
    Class to represent an in-RAM collection of objects
    '''
    def __init__(self, name, schema):
        '''
        In:
            name - dataset name - e.g. 'animal'
            schema - dataset schema
        '''
        super().__init__(name, schema) 
        self.data = dict()
        return

    def get(self, id):
        '''
        Access the record by id
        '''
        return self.data.get(id, None)
        
    def put_(self, id, dat):
        '''
        Stores data into the dataset
        Returns:
            True if dat is validated against schema and is added to the dataset
            False otherwise
        May throw:
            SchemaError
        '''
        self.data[id] = dat
        return True


class DataSetCouchDB(DataSet):
    '''
    Class to represent an in-CouchDB collection of objects
    '''
    def __init__(self, name, schema, url):
        '''
        In:
            name - dataset name - e.g. 'animal'
            schema - dataset schema
            url - CouchDB URL
        '''
        super().__init__(name, schema)
        self.ses = Session()
        self.url = url
        self.db_name = 'db_' + name
        self.db_exists = False
        #
        # verify that the database exists, if not - create it
        #
        url = self.url + '/' + self.db_name
        resp = self.ses.head(url)
        log.info('ses.head(%s) => %d', url, resp.status_code)
        if(resp.status_code == 404):
            #
            # database does not exist - create it!
            #
            resp = self.ses.put(url)
            log.info('ses.put(%s) => %d', url, resp.status_code)
            if(resp.status_code == 201):
                # created!
                self.db_exists = True
                pass
            elif(resp.status_code == 400):
                # bad db name
                pass
            elif(resp.status_code == 401):
                # unauthorized
                pass
            elif(resp.status_code == 412):
                # db already exists!
                pass
        elif(resp.status_code == 200):
            # database does exist - we're good!
            self.db_exists = True
        else:
            pass
        return

    def get(self, id):
        '''
        Access the record by id
        '''
        if(not self.db_exists):
            return None

        url = self.url + '/' + self.db_name + '/' + id
        resp = self.ses.get(url)
        log.debug('ses.get(%s) => %d', url, resp.status_code)
        if(resp.status_code != 200):
            return None
        res = resp.json()
        del res[ '_id' ]
        del res[ '_rev' ]
        log.info('get(%s) => %s', id, str(res))
        return res 

    def put_(self, id, dat):
        '''
        Stores data into the dataset
        Returns:
            True if dat is validated against schema and is added to the dataset
            False otherwise
        May throw:
            Error
        '''
        if(not self.db_exists):
            return None
        url = self.url + '/' + self.db_name + '/' + id
        resp = self.ses.put(url, json=dat)
        log.debug('ses.put(%s, %s) => %d', url, str(dat), resp.status_code)
        if(resp.status_code == 201):
            log.info('put_(%s) => %s', id, str(dat))
            return dat
        elif(resp.status_code == 202):
            log.info('put_(%s) => %s', id, str(dat))
            return dat
        log.info('put_(%s) => None', id)
        return None

# we will be storing animals here
theAnimals = None

def init_dataset(aconfig):
    '''
    In:
        aconfig is an app config dictionary.
    SideEffect:
        assigns an object to theAnimals
    '''
    global theAnimals
    dstore = aconfig.get('DATASTORE')
    if(dstore == 'RAM'):
        log.info('DATASTORE is RAM')
        theAnimals = DataSetRAM('animal', AnimalSchema)
        return True

    elif(dstore == 'CouchDB'):
        log.info('DATASTORE is CouchDB')
        url = aconfig.get('COUCHDB_URL')
        if not url:
            log.info('No COUCHDB_URL')
            return False
        log.info('COUCHDB_URL=%s', str(url))
        theAnimals = DataSetCouchDB('animal', AnimalSchema, url)
        return True

    # no datastore that we would understand!
    log.error('Unknown DATASTORE %s', dstore)
    return False
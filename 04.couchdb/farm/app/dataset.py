from requests import Session
from abc import ABC, abstractmethod

# For relative imports to work in Python 3.6
# import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import os
import sys
from app.logger import log
from .farm_schema import AnimalSchema

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# assert log is not None


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
        Returns:<
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

    @abstractmethod
    def pop(self, id):
        '''
        Removes the record identified by id from the dataset
        Returns the data (if found) or None.
        '''
        pass

    @abstractmethod
    def ids(self):
        '''
        Returns iterator by all doc ids
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

    def pop(self, id):
        '''
        Removes the record identified by id from the dataset.
        Returns the data (if found) or None.
        '''
        return self.data.pop(id, None)

    def ids(self):
        '''
        Returns iterator by all doc ids
        '''
        return self.data.keys()


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
        # TCP session to talk to CouchDB
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
        if resp.status_code == 404:
            #
            # database does not exist - create it!
            #
            resp = self.ses.put(url)
            log.info('ses.put(%s) => %d', url, resp.status_code)
            if resp.status_code == 201:
                # created!
                self.db_exists = True
                pass
            elif resp.status_code == 400:
                # bad db name
                pass
            elif resp.status_code == 401:
                # unauthorized
                pass
            elif resp.status_code == 412:
                # db already exists!
                pass
        elif resp.status_code == 200:
            # database does exist - we're good!
            self.db_exists = True
        else:
            pass
        return

    def get(self, id):
        '''
        Access the record by id
        '''
        if not self.db_exists:
            return None

        url = self.url + '/' + self.db_name + '/' + id
        resp = self.ses.get(url)
        log.debug('ses.get(%s) => %d', url, resp.status_code)
        if resp.status_code != 200:
            return None
        res = resp.json()
        del res['_id']
        del res['_rev']
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
        if not self.db_exists:
            return None
        url = self.url + '/' + self.db_name + '/' + id
        resp = self.ses.put(url, json=dat)
        log.debug('ses.put(%s, %s) => %d', url, str(dat), resp.status_code)
        if resp.status_code == 201:
            log.info('put_(%s) => %s', id, str(dat))
            return dat
        elif resp.status_code == 202:
            log.info('put_(%s) => %s', id, str(dat))
            return dat
        log.info('put_(%s) => None', id)
        return None

    def pop(self, id):
        '''
        Removes the record identified by id from the dataset.
        Returns the data (if found) or None.
        '''
        if not self.db_exists:
            return None
        url = self.url + '/' + self.db_name + '/' + id
        # first get it from the DB
        resp = self.ses.get(url)
        log.debug('ses.get(%s) => %d', url, resp.status_code)
        if resp.status_code != 200:
            return None
        res = resp.json()
        del res['_id']
        rev = res.pop('_rev', None)
        if rev is None:
            return None

        # now let's delete it!
        url = url + '?rev=' + rev
        resp = self.ses.delete(url)
        log.debug('ses.delete(%s) => %d', url, resp.status_code)
        log.info('pop(%s) => %s', id, str(res))
        return res

    def ids(self):
        '''
        Returns iterator by all doc ids
        '''
        if not self.db_exists:
            return []
        # get the list of all the docs from the DB
        url = self.url + '/' + self.db_name + '/_all_docs'
        resp = self.ses.get(url)
        log.debug('ses.get(%s) => %d', url, resp.status_code)
        if resp.status_code != 200:
            return []
        res = resp.json()
        return [row['id'] for row in res.get('rows', [])]


# we will be storing animals here
theAnimals = None


def init_dataset(aconfig):
    '''
    In:
        aconfig is an app config dictionary.
    SideEffect:
        assigns an object to theAnimals
    Returns:
        True is succeeds
    '''
    global theAnimals
    dstore = aconfig.get('DATASTORE')
    if dstore == 'RAM':
        log.info('DATASTORE is RAM')
        theAnimals = DataSetRAM('animal', AnimalSchema)
        return True

    elif dstore == 'CouchDB':
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

import logging
from datetime import datetime
from .exceptions import DoesNotExist, MultipleObjectsReturned
from .data import language_codes

logger = logging.getLogger(__name__)

class Model(object):
    def __init__(self, data, collection):
        self._collection = collection
        self.conn = collection.conn
        self.data = self.format_data(self.set_defaults(data))
        self.doc_type = self._collection.doc_type
        self.index = self._collection.index


    def _index(self, **kwargs):
        if 'force_new' in kwargs or 'id' not in kwargs:
            kwargs['op_type'] = 'create'
            del kwargs['force_new']

        kwargs['index'] = self.index
        kwargs['doc_type'] = self.doc_type

        print kwargs

        return self.conn.index(**kwargs)


    def save(self, upsert_params = [], force_new=False, refresh=False):
        if force_new:
            return self._index(body=self.data, force_new=True, refresh=refresh)
        else:
            return self.upsert(params=upsert_params, refresh=refresh)

    
    def upsert(self, params = [], refresh=False):
        if params:
            logger.info("Have params")
            try:
                doc = self._collection.get(params)
                return self._index(body=self.data, id=doc['id'], 
                    refresh=refresh)
            except DoesNotExist:
                logger.info("Did not find doc for " + str(params))
                return self._index(body=self.data, force_new=True, 
                    refresh=refresh)
            except MultipleObjectsReturned:
                logger.info("Got more than one object for "+str(params))
                return None

        else:
            logger.info("Upsert called without params")
            return self._index(body=self.data, force_new=True, 
                refresh=refresh)


    def format_data(self, data):
        return data

    def set_defaults(self, data):
        return data


class Item(Model):
    def set_defaults(self, data):
        defaults = {
            'license': 'unknown',
            'lifespan': 'temporary',
            'createdAt': datetime.now()
        }

        for key,val in defaults.iteritems():
            if key not in data:
                data[key] = val

        return data


    def save(self, refresh=False):
        upsert_params = [
            {
                'field':'remoteID',
                'value': self.data['remoteID']
            },
            {
                'field': 'source',
                'value': self.data['source']
            }
        ]

        return super(Item, self).save(upsert_params=upsert_params, 
            refresh=refresh)


    def format_data(self, data):
        data['updatedAt'] = datetime.now()

        if 'publishedAt' not in data:
            data['publishedAt'] = data['createdAt']

        if 'language' in data and 'code' in data['language']:
            if data['language']['code'] in language_codes.codes:
                data['language'] = language_codes[data['language']['code']]


        data['searchText'] = ''

        if 'content' in data:
            data['searchText'] = data['content']

        if 'summary' in data:
            data['searchText'] += ' ' + data['summary']

        if 'contentEnglish' in data:
            data['searchText'] += ' ' + data['contentEnglish']

        if 'entities' in data:
            data['searchText'] += ' ' + ' '.join(data['entities'])

        if 'tags' in data:
            data['searchText'] += ' ' + ' '.join([tag['name'] for tag in data['tags']])

        #data['searchText'] = search_text

        return data

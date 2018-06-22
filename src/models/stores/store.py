import re
import uuid
from src.common.database import Database
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreErrors


class Store(object):
    def __init__(self, name, url_prefix, price_tag_name, price_query, name_tag_name, name_query, _id=None):
        self.name = name
        self. url_prefix = url_prefix
        self.price_tag_name = price_tag_name
        self.price_query = price_query
        self.name_tag_name = name_tag_name
        self.name_query = name_query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "price_tag_name": self.price_tag_name,
            "price_query": self.price_query,
            "name_tag_name": self.name_tag_name,
            "name_query": self.name_query
        }

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"_id": id}))

    def save_to_mongo(self):
        Database.update(StoreConstants.COLLECTION, {"_id": self._id}, self.json())

    @classmethod
    def get_by_name(cls, store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"name": store_name}))

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"url_prefix": {"$regex": '^{}'.format(url_prefix)}}))

    @classmethod
    def find_by_url(cls, url):
        # for i in range(0, len(url)):
        #     try:
        #         store = cls.get_by_url_prefix(url[:i])
        #         return store
        #     except:
        #         raise StoreErrors.StoreNotFoundException("URL prefix for that store is not found.")
        pattern = re.compile(r'^(?P<url_prefix>[^:]*://[^/]+)')
        match = pattern.match(url)
        if match:
            return cls.get_by_url_prefix(match.group('url_prefix'))
        raise StoreErrors.StoreNotFoundError("No store with the specified URL {} found.".format(url))

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION, {})]

    def delete(self):
        Database.remove(StoreConstants.COLLECTION, {'_id': self._id})

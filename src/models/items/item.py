import uuid
import requests
from bs4 import BeautifulSoup
import re
from src.common.database import Database
import src.models.items.constants as ItemConstants
from src.models.stores.store import Store


class Item(object):
    def __init__(self, url, name=None, price=None, _id=None):
        self.url = url
        store = Store.find_by_url(url)
        self.price_tag_name = store.price_tag_name
        self.price_query = store.price_query
        self.name_tag_name = store.name_tag_name
        self.name_query = store.name_query
        self.price = None if price is None else price
        self.name = None if name is None else name
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.price_tag_name, self.price_query)
        string_price = element.text.strip()

        pattern = re.compile("(\d+.\d+)")
        match = pattern.search(string_price)
        self.price = float(match.group().replace(',', '.'))

        return self.price

    def load_name(self):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.name_tag_name, self.name_query)
        string_name = element.text.strip()
        self.name = string_name

        return self.name

    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            'url': self.url,
            '_id': self._id,
            'name': self.name,
            'price': self.price
        }

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))

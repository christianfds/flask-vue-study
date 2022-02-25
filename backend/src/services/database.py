from config import config
from pymongo import MongoClient

_mongo_uri = config.get('mongo').get('uri')
mongo_conn = MongoClient(_mongo_uri)
mongo_database = mongo_conn.get_database(config.get('mongo').get('default_database'))
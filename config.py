import os
from pymongo import MongoClient


class Config(object):
    # Application
    APP_DIR = os.path.dirname(os.path.realpath(__file__))
    TEMPLATES_DIR = os.path.join(APP_DIR, 'view')
    STATIC_DIR = os.path.join(APP_DIR, 'view', 'static')
    LOGFILE = os.path.join(APP_DIR, 'flask.log')
    DEBUG = True
    FLASK_SECRET_KEY = 'the-most-secret-key-in-the-secret-world-of-secret-keys'

    # OMDb API
    OMDB_URL = 'http://www.omdbapi.com/'
    OMDB_API_KEY = 'e92e6f00'

    # MongoDB
    mongo_client = None
    MONGODB_URL = 'mongodb://localhost:27017'

    @staticmethod
    def _connect_mongodb():
        """
        Connect to the MongoDB
        """
        try:
            Config.mongo_client = MongoClient(Config.MONGODB_URL)
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def init():
        """
        Initialise the web application
        """
        Config._connect_mongodb()

        print('Finished start-up tasks.')
import requests
from requests.sessions import merge_setting, session

from config import Config


class InvalidParamsException(Exception):
    """
    Invalid query string argument (parameters) sent to the OMDb API.
    """
    pass


class IMDb():
    def __init__(self):
        if type(self) is IMDb:
            raise Exception('This class "{}" should not be instantiated.'.format(IMDb.__str__(self)))

    @staticmethod
    def remove_mongo_id(d):
        """
        Remove the MongoDB dict key '_id' storing the MongoDB ObjectId.

        :param d: A dict of some IMDb resource.
        :return: A dict without the key '_id'.
        :rtype: dict
        """
        if '_id' in d:
            del d['_id']
        return d

    @staticmethod
    def query(url, params=None):
        if 'i' in params: # if params contains 'i' (imdbID), then get the imdb resource instance
            return IMDb._get_imdb_instance(url, params)
        elif 's' in params:
            return IMDb._get_imdb_register(url, params)
        else:
            raise InvalidParamsException('The request does not contain arguments for a title (s) or IMDb ID (i).')

    @staticmethod
    def _build_url_query_id(url, params):
        """
        Build the url and params into a valid HTTP URL.

        :param url: The OMDb API URL.
        :param params: The query string arguments.
        :return: A valid HTTP URL with encoded query string arguments.
        :rtype: str
        """
        id = url
        if id[-1] == '/':
            id = id[:len(id)-1] # remove the trailing slash for id consistency
        for k, v in params.items():
            if '?' not in id:
                id += '?' + k + '=' + v
            else:
                id += '&' + k + '=' + v
        return id

    @staticmethod
    def _get_imdb_register(url, params):
        """
        Retrieve an IMDb register of instances using url + params as a unique identifier.

        :param url: The OMDb API's URL.
        :param params: A dict of the query string arguments.
        :return: An IMDb register of instances.
        :rtype: dict
        """

        # Retrieve from MongoDB
        registers = Config.mongo_client.imdb.registers
        # Build the unique identifier (url + query)
        id = IMDb._build_url_query_id(url, params)
        result = registers.find_one({'url_id': id})

        if result is not None:
            return IMDb.remove_mongo_id(result)

        # Retrieve from the OMDb API
        r = requests.get(url, params=params)
        response = r.json()
        if response['Response'] == 'True':
            # store it in MongoDB before returning the result
            # add the url_id
            response['url_id'] = id
            registers.insert_one(response)
            # The insert_one() changes the original response dict. It now has an extra key '_id' inserted
            # by MongoDB. We need to remove it before returning the result.
            return IMDb.remove_mongo_id(response)
        else:
            # TODO: store the failed id in MongoDB
            raise InvalidParamsException(response['Error'])

    @staticmethod
    def _get_imdb_instance(url, params):
        """
        Retrieve an IMDb instance using its unique imdbID identifier.

        :param url: The OMDb API's URL.
        :param params: A dict of the query string arguments.
        :return: An IMDb instance's metadata as a dict.
        :rtype: dict
        :raises: InvalidParamsException
        """

        # retrieve from MongoDB
        instances = Config.mongo_client.imdb.instances
        result = instances.find_one({'imdbID': params['i']}) # search MongoDB for the imdbID

        if result is not None:
            return IMDb.remove_mongo_id(result)

        # retrieve from OMDb API
        r = requests.get(url, params=params)
        response = r.json()
        if response['Response'] == 'True':
            # store it in MongoDB before returning the result
            instances.insert_one(response)
            # The insert_one() changes the original response dict. It now has an extra key '_id' inserted
            # by MongoDB. We need to remove it before returning the result.
            return IMDb.remove_mongo_id(response)
        else:
            # TODO: store the failed id in MongoDB
            raise InvalidParamsException(response['Error'])
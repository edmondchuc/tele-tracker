from flask_login import UserMixin
from config import Config


class User(UserMixin):
    def __init__(self, username, email, password_hash):
        self._id = username
        self._email = email
        self._password_hash = password_hash

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def password_hash(self):
        return self._password_hash

    def __repr__(self):
        return 'model.user.User:{} {}'.format(self.id, self.email)

    def __str__(self):
        return 'username: {} email: {}'.format(self.id, self.email)

    #
    # -- Static methods of User ----------------------------------------------------------------------------------------
    #
    @staticmethod
    def get_users():
        instances = Config.mongo_client.users.instances
        users = instances.find()
        return users

    @staticmethod
    def create_user(username, email, password_hash):
        instances = Config.mongo_client.users.instances
        instances.insert_one({'username': username, 'email': email, 'password_hash': password_hash})
        return User(username, email, password_hash)

    @staticmethod
    def get_user(id):
        instances = Config.mongo_client.users.instances
        user = instances.find_one({'email': id})
        if user:
            return User(user['username'], user['email'], user['password_hash'])
        user = instances.find_one({'username': id})
        if user:
            return User(user['username'], user['email'], user['password_hash'])

    @staticmethod
    def get_user_by_email(email):
        instances = Config.mongo_client.users.instances
        user = instances.find_one({'email': email})
        if user:
            return User(user['username'], user['email'], user['password_hash'])
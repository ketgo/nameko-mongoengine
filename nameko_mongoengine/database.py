"""
    Database interface for dependency
"""

from mongoengine.connection import get_db


class Database:
    """
        Database interface
    """

    def __init__(self, alias):
        self._alias = alias

    @property
    def db(self):
        """
            Returns PyMongo database connection interface
        """
        return get_db(self._alias)

    @classmethod
    def with_alias(cls, alias):
        """
            Returns interface instance for new MongoEngine connection alias
        """
        return cls(alias)

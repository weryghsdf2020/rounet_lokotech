"""
    Provides class `DataBase` that handles database connection
"""
from pymongo import MongoClient


class DataBase():
    """
        Connects to the database
    """

    def __init__(self, db_config):
        self.config = db_config

        self.client = MongoClient(self.config['host'],
                                  self.config['port'])
        self.db = self.client[self.config['database']]

    def drop_table(self, col_name):

        if col_name in self.db.list_collection_names():

            self.db[col_name].drop()
            print(
                f'collection "{col_name}" succecfully drop in {self.db.name}')
        else:
            print(f'collection "{col_name}" not in {self.db.name}')

    def init_db(self):
        """
            Init database
        """
        pass

    def connect(self):
        """
            Connects to the database
        """
        pass

    def make_session(self):
        """
            Wraps session creation process
        """
        pass

    def add(self):
        """
            Adds object to session
        """
        pass

    def commit(self):
        """
            Wrapper for self.session.commit()
        """
        pass

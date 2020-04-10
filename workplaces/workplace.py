

from workplaces.db import DataBase

from data_providers.provider import DataProvider


class WorkPlace():
    """
        Base class for workplaces.
    """

    instance = None

    def __init__(self, name: str, config: dict, db_type: str):
        self.name = name
        self.config = config

        self.db = DataBase(config['db_configs'][db_type])
        self.data_provider = DataProvider(self)
        self.loaders = []
        self.source_list = self.config['source_list']

        WorkPlace.instance = self

        self._load_loaders()

    def _load_loaders(self):
        for Loader in self.config['loaders']:
            loader = Loader(self)
            self.loaders.append(loader)
            self.data_provider.add_loader(loader)

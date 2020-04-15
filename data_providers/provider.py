import pandas as pd

from utils import first_or_none


class DataProvider:
    """Assigns loaders to return data to the controller
    """

    def __init__(self, parent, provides=None, loaders=None):
        self.parent = parent
        self.provides = provides
        if not loaders:
            loaders = []
        self.loaders = loaders

    def get_dataset(self,
                    dataset_name: str,
                    source_type: str = 'mongo',
                    dataset_source: str = 'mongo',
                    **kwargs
                    ):
        """Loads data from loaders

        Parameters
        ----------
        dataset_name : str
        source_type : str
        dataset_source : str

        Returns
        -------
        data: dict or pd.DataFrame
        """
        loader = first_or_none(
            self.loaders,
            lambda x: x.source_type == source_type
        )

        if not loader:
            print('Загрузчики не добавлены при инициации рабочей области')

        if 'version_name' in kwargs and 'transport_type' not in kwargs:
            # print(1)
            version_name = kwargs['version_name']
            data = loader.load_data(dataset_source,
                                    dataset_name,
                                    version_name=version_name)
        elif 'transport_type' in kwargs and 'version_name' not in kwargs:
            # print(2)
            transport_type = kwargs['transport_type']
            data = loader.load_data(dataset_source,
                                    dataset_name,
                                    transport_type=transport_type)
        elif 'transport_type' in kwargs and 'version_name' in kwargs:
            # print(3)
            transport_type = kwargs['transport_type']
            version_name = kwargs['version_name']
            data = loader.load_data(dataset_source,
                                    dataset_name,
                                    version_name=version_name,
                                    transport_type=transport_type)
        else:
            # print(4)
            data = loader.load_data(dataset_source, dataset_name)

        return data

    def save_dataset(self, dataset,
                     output_type: str = 'mongo',
                     **kwargs):
        """saves data according to its output type
        """

        loader = first_or_none(
            self.loaders,
            lambda x: x.source_type == output_type
        )
        if loader:
            if output_type == 'mongo':
                collection_name = kwargs.get('collection_name')
                if 'version_name' in kwargs and 'transport_type' not in kwargs:
                    version_name = kwargs['version_name']
                    loader.save_data(dataset, collection_name,
                                     version_name=version_name)
                elif 'transport_type' in kwargs and 'version_name' not in kwargs:
                    transport_type = kwargs['transport_type']
                    loader.save_data(dataset, collection_name,
                                     transport_type=transport_type)
                elif 'transport_type' in kwargs and 'version_name' in kwargs:
                    transport_type = kwargs['transport_type']
                    version_name = kwargs['version_name']
                    loader.save_data(dataset, collection_name,
                                     version_name=version_name,
                                     transport_type=transport_type)
                else:
                    loader.save_data(dataset, collection_name)
            elif output_type == 'Excel' or output_type == 'CSV':
                flname = kwargs.get('flname')
                path = kwargs.get('path')
                geometry_column = kwargs.get('geometry_column')
                loader.save_data(dataset, flname, path)
            elif output_type == 'QGSLayers':
                loader.save_data(dataset, geometry_column, flname)

    def add_loader(self, loader):
        self.loaders.append(loader)

    def remove_loader(self):
        pass

    def reset_loader(self):
        pass

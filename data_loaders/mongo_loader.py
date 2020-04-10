import pandas as pd

from workplaces.workplace import WorkPlace


class MongoLoader:

    def __init__(self, wp,
                 dataset: str = None,
                 fname: str = None):
        self.wp = wp
        self.dataset = dataset
        self.fname = fname
        self.source_type = 'mongo'

    def load_data(self,
                  dataset_source: str,
                  dataset_name: str, version_name=None):
        """Loads data from db
        """
        if version_name:
            # print(1, version_name)
            # print(self.wp.db.db[dataset_name].find_one().keys())
            data = [x for x in self.wp.db.db[dataset_name].find(
                {'version': version_name})]
        else:
            # print(2)
            data = [x for x in self.wp.db.db[dataset_name].find()]

        if dataset_name in self.wp.config['dataset_load_convert_func'].keys():

            convert_func = self.wp.config['dataset_load_convert_func'][dataset_name]
            res = convert_func(data)
        else:
            res = data
        return res

    def save_data(self,
                  dataset,
                  collection_name: str, version_name=None, **kwargs):
        if collection_name not in self.wp.db.db.list_collection_names():
            collection = self.wp.db.db.create_collection(
                collection_name)
        else:
            collection = self.wp.db.db[collection_name]
        if isinstance(dataset, pd.DataFrame):
            if 'inv_col_names' in kwargs:
                dataset = dataset[[x for x in dataset.columns
                                   if x not in kwargs['inv_col_names']]]

            df_numpy = dataset.to_numpy()
            Column_Index_Dictionary = dict(zip(list(range(0, len(dataset.columns))),
                                               dataset.columns))

            insert_list = []

            for each in df_numpy:
                row = {}
                for i, val in enumerate(each):
                    row[Column_Index_Dictionary[i]] = val
                insert_list.append(row)
        elif isinstance(dataset, list):
            insert_list = dataset
        elif isinstance(dataset, dict):
            insert_list = [{key: val} for key, val in dataset.items()]

        if version_name:
            # print(3)

            _insert_list = []

            # x_0 = insert_list[0]
            # print(x_0.keys())
            for x in insert_list:

                for key, val in x.items():
                    _item = {key: val,
                             'version': version_name}

                    # val.update({'version': version_name})
                    _insert_list.append(_item)

            insert_list = _insert_list

        collection.insert_many(insert_list)

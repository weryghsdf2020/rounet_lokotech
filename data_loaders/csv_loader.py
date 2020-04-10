import pandas as pd


class CSVLoader:

    def __init__(self, wp, dataset: str = None, fname: str = None):
        self.wp = wp
        self.dataset = dataset
        self.fname = fname
        self.source_type = 'CSV'
        self.data: pd.DataFrame = None

    def load_data(self,
                  dataset_source,
                  dataset_name):
        pass

    def save_data(self):
        pass

    def _load_csv(self):
        pass

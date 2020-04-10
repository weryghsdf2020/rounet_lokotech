import pandas as pd


class ExcelLoader:

    def __init__(self, wp,
                 dataset: str = None,
                 fname: str = None):
        self.wp = wp
        self.dataset = dataset
        self.fname = fname
        self.source_type = 'Excel'
        self.data: pd.DataFrame = None

    def _load_excel(self):
        pass

    def load_data(self,
                  dataset_source: str,
                  dataset_name: str):
        """Loads data from Excel into a dataframe for provider
        """
        pass

    def save_data(self,
                  dataset: pd.DataFrame,
                  fname: str,
                  path: str):
        pass

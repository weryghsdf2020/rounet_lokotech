import pandas as pd


class Forecast():

    def __init__(self, tr_soc_df: pd.DataFrame,
                 tr_geometries: dict,
                 flows_df: pd.DataFrame):
        self.tr_soc_df = tr_soc_df
        self.tr_geometries = tr_geometries
        self.flows_df = flows_df

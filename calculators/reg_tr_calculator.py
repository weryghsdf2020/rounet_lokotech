import numpy as np
import pandas as pd

from shapely.ops import cascaded_union

from converters.converter_for_mongo import convert_mos_list_to_df

YEARS = [2018, 2019, 2020, 2021, 2022,
         2023, 2024, 2025, 2026, 2027,
         2028, 2029, 2030, 2031, 2032,
         2033, 2034, 2035]

SOC_TYPES = ['POP', 'EMPLOY', 'GRP', 'INCOME', 'BED']


class TR_calculator():

    """
        Обеспечивает формирование транспортных районов 
            из муниципальных
    """

    def __init__(self, municipalities: pd.DataFrame):

        self.municipalities = municipalities

        self.subscribers = []

        self.trs = {}

    def generate_tr(self):
        """

        """

        mun_df = self.municipalities
        trs_names = mun_df['tr'].drop_duplicates().values

        for its_code, tr_name in enumerate(trs_names):

            tr_contain = {}
            rec = mun_df[mun_df['tr'] == tr_name]

            for soc_type in SOC_TYPES:
                soc_type_contain = {}
                rec_soc = rec[rec['soc_type'] == soc_type]

                for year in YEARS:

                    _values = rec_soc[str(year)].values
                    if soc_type != 'INCOME':

                        val = sum(_values)

                    else:
                        pops_values = rec[rec['soc_type']
                                          == 'POP'][str(year)].values
                        val = np.average(_values,
                                         weights=pops_values)

                    soc_type_contain[str(year)] = val

                tr_contain[str(soc_type)] = soc_type_contain

            tr_contain['tr_name'] = tr_name
            tr_contain['geometry'] = cascaded_union(
                list(rec.geometry.values)).to_wkt()

            self.trs[str(its_code)] = tr_contain

    def add_subscriber(self, sub):
        self.subscribers.append(sub)

    def notify(self, event_type, *args):
        for subscriber in self.subscribers:
            subscriber.update(event_type, *args)

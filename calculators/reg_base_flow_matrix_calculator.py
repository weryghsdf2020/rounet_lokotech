import pandas as pd
from shapely.geometry import Point, LineString, Polygon, mapping
import numpy as np

# from config import defaults

# # Общий транспортный район не РФ
# default_tr_id = defaults['default_tr_info']['default_tr_id']
# default_tr_name = defaults['default_tr_info']['default_tr_name']


class RegBaseFlowCalc():

    """
        Обеспечивает формирование матрицы корреспонденций 
            из базы потоков между транспортными районами
    """

    def __init__(self, trs: dict,
                 flows_base: pd.DataFrame,
                 plos_express_info: dict):

        self.trs = trs
        self.flows_base = flows_base
        self.plos_express_info = plos_express_info
        self.df_matrix = None
        self.save_dict = None

        self.subscribers = []
        self.default_tr_id = max([key for key, val in trs.items()])+1

        # self.trs = {}

    def _assign_plos_to_tr(self):
        plo_express_dict = {}
        for _plo, info in self.plos_express_info.items():
            plo_express_dict[_plo] = {'geometry': info['geometry'],
                                      'tr_id': self._bind_plo_tr(info['geometry'])
                                      }
            # info.update({'tr': self._bind_plo_tr(info['geometry'])})
        self.plos_express_info = plo_express_dict
        # print('ок')

    def _bind_plo_tr(self, point: Point):
        tr = self.default_tr_id
        for tr_id, tr_info in self.trs.items():
            if tr_info['geometry'].intersects(point):
                tr = tr_id
        return tr

    def generate_base_matrix(self):
        """

        """
        self._assign_plos_to_tr()
        # print('привязка завершена')
        self.flows_base['tr_source_id'] = [self.plos_express_info[x.plo_source_flow_express]['tr_id']

                                           for x in self.flows_base.itertuples()]
        self.flows_base['tr_target_id'] = [self.plos_express_info[x.plo_target_flow_express]['tr_id']

                                           for x in self.flows_base.itertuples()]
        df_grouped = self.flows_base[['tr_source_id', 'tr_target_id',
                                      'flows']].groupby(['tr_source_id',
                                                         'tr_target_id'], as_index=False).sum()

        _maximum_index = self.default_tr_id+1

        matrix = np.zeros((_maximum_index, _maximum_index), dtype=float)

        for x in df_grouped.itertuples():
            matrix[int(x.tr_source_id)][int(x.tr_target_id)] = x.flows

        df_matrix = pd.DataFrame(matrix,
                                 columns=[str(i)
                                          for i in range(len(matrix))],
                                 index=[str(i) for i in range(len(matrix))])

        self.df_matrix = df_matrix
        self._make_dict_save_format()

    def _make_dict_save_format(self):
        self.save_dict = {str(i): list(x)
                          for i, x in self.df_matrix.iterrows()}

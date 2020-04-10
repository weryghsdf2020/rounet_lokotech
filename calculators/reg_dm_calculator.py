import pandas as pd
from shapely.geometry import Point, LineString, Polygon, mapping
import numpy as np
from utils import row_orthodromy


# Расстояние до иностранного ТР
DEFAULT_DIST = 10000


class RegDMCalc():

    """
        Обеспечивает формирование матрицы расстояний 
            из базы потоков между транспортными районами
    """

    def __init__(self, trs: dict,
                 flows_base=None,
                 plos_express_info=None,
                 calc_type='by_ort'):

        self.trs = trs
        self.flows_base = flows_base
        self.plos_express_info = plos_express_info
        self.calc_type = calc_type
        self.df_matrix = None
        self.save_dict = None

        self.subscribers = []
        self.default_tr_id = max([key for key, val in trs.items()])+1

    def generate_dm(self):

        if self.calc_type == 'by_ort':
            lats, longs = [], []
            for _tr_id, info in self.trs.items():
                poly = info['geometry']
                centroid = poly.centroid
                lats.append(centroid.y)
                longs.append(centroid.x)

            dm = row_orthodromy(np.array(lats), np.array(longs))
            # print(len(dm))
            dm = self._add_foreign_tr_info(dm, DEFAULT_DIST)
            # print(len(dm))
            self.df_matrix = pd.DataFrame(dm,
                                          columns=[str(i)
                                                   for i in range(len(dm))],
                                          index=[str(i) for i in range(len(dm))])
            self._make_dict_save_format()

    def _add_foreign_tr_info(self, dm, default_value_dist):
        new_dm = np.zeros((dm.shape[0]+1,
                           dm.shape[1]+1), dtype=float)
        for i in range(len(new_dm)):
            for j in range(len(new_dm)):
                if i == j:
                    val = 0
                else:
                    try:
                        val = dm[i][j]
                    except:
                        val = default_value_dist
                new_dm[i][j] = val
        return new_dm

    def _make_dict_save_format(self):
        self.save_dict = {str(i): list(x)
                          for i, x in self.df_matrix.iterrows()}

    def _assign_plos_to_tr(self):
        plo_express_dict = {}
        for _plo, info in self.plos_express_info.items():
            plo_express_dict[_plo] = {'geometry': info['geometry'],
                                      'tr_id': self._bind_plo_tr(info['geometry'])
                                      }

        self.plos_express_info = plo_express_dict

    def _bind_plo_tr(self, point: Point):
        tr = self.default_tr_id
        for tr_id, tr_info in self.trs.items():
            if tr_info['geometry'].intersects(point):
                tr = tr_id
        return tr

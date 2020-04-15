import pandas as pd
import numpy as np

from config import defaults

TR_TYPES = defaults['reg_transport_types']


class RegForecastPotentialsCalc():

    def __init__(self, trs: dict,
                 base_matrix: dict,
                 base_year: int,
                 forecast_year: int,
                 tr_type: str,
                 elasticities: dict):
        self.trs = trs
        self.base_matrix = base_matrix
        self.base_year = base_year
        self.forecast_year = forecast_year
        self.tr_type = tr_type
        self.elasticities = elasticities

        # self.base_full_matrix = None

        self.base_attractions = None
        self.base_generations = None

        self.forecast_attractions = None
        self.forecast_generations = None

    def calc_forecast_potentials(self):
        # self._calc_base_full_matrix()
        self._calc_base_potentials()

        pop_indicies = self._get_indicies('POP')
        employ_indicies = self._get_indicies('EMPLOY')
        grp_indicies = self._get_indicies('GRP')

        # elasticities_grp_attraction
        ega = np.array(
            [self.elasticities['GRP'][self.tr_type][str(self.forecast_year)]
             for i in range(len(self.base_matrix))])
        # elasticities_grp_generation
        egg = ega

        generation_indicies = self.calc_generation_indicies(
            pop_indicies, grp_indicies, employ_indicies, egg)
        attraction_indicies = self.calc_attraction_indicies(
            pop_indicies, grp_indicies, employ_indicies, ega)

        self.forecast_generations = self.base_generations*generation_indicies
        self.forecast_attractions = self.base_attractions*attraction_indicies

    def _calc_base_potentials(self):

        self.base_attractions = (np.sum(self.base_matrix, axis=1) +
                                 np.sum(self.base_matrix, axis=0))/2
        self.base_generations = self.base_attractions

    def _get_indicies(self, soc_type, default_val=0.001):
        contain = []
        for _key, val in self.trs.items():
            base_val = val[soc_type][str(self.base_year)]
            forecast_val = val[soc_type][str(self.forecast_year)]

            if not base_val:
                base_val = default_val
            if not forecast_val:
                forecast_val = default_val
            index = forecast_val/base_val
            contain.append(index)
        # Дли иностранного ТР
        contain.append(np.mean(np.array(contain)))
        res = np.array(contain)
        return res

    def calc_generation_indicies(self, pop_indicies, grp_indicies, employ_indicies, egg):
        g1 = np.array([pop_indicies[i] *
                       (1+egg[i]*(grp_indicies[i]-1))
                       for i in range(len(pop_indicies))])
        g2 = np.array([employ_indicies[i] *
                       (1+egg[i]*(grp_indicies[i]-1))
                       for i in range(len(pop_indicies))])

        res = (g1+g2)/2
        return res

    def calc_attraction_indicies(self, pop_indicies, grp_indicies, employ_indicies, ega):
        # at = np.array([bed_indicies[i] *
        #                (1+ega[i]*(grp_indicies[i]-1))
        #                for i in range(len(pop_indicies))])
        a1 = np.array([employ_indicies[i] *
                       (1+ega[i]*(grp_indicies[i]-1))
                       for i in range(len(pop_indicies))])
        a2 = np.array([pop_indicies[i] *
                       (1+ega[i]*(grp_indicies[i]-1))
                       for i in range(len(pop_indicies))])

        res = (a1+a2)/2
        return res

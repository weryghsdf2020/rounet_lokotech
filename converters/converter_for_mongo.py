import pandas as pd
import numpy as np
from shapely.wkt import loads as gload

from utils import first_or_none


def convert_mos_list_to_df(mo_list: list):
    """
        Разворачивает список по мо в df
    """

    df_contain = []
    for mo_dict in mo_list:
        its_code = first_or_none(list(mo_dict.keys()),
                                 lambda x: x != '_id')
        mo_info = mo_dict[its_code]

        mo_df = pd.DataFrame(mo_info)
        mo_df['soc_type'] = mo_df.index
        mo_df['its_code'] = [its_code for x in range(len(mo_df))]
        mo_df['geometry'] = [gload(x.geometry_wkt)
                             for x in mo_df.itertuples()]
        mo_df = mo_df.reset_index()

        mo_df = mo_df[['its_code', 'oktmo', 'tr', 'sub_name', 'mun_name',
                       'mun_center_name', 'soc_type', 'geometry',
                       '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026',
                       '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']]
        df_contain.append(mo_df)
    mos_df = pd.concat(df_contain, ignore_index=True)

    return mos_df


def convert_trs_to_valid_format(trs_list: list):

    trs_contain = {}

    for tr_dict in trs_list:
        its_code = first_or_none(list(tr_dict.keys()),
                                 lambda x: x != '_id' and x != 'version')
        tr_info = tr_dict[its_code]
        _tr_dict = {}

        for key, val in tr_info.items():
            if key != 'version':
                if key == 'geometry':
                    val = gload(val)

                _tr_dict[key] = val

        trs_contain[int(its_code)] = _tr_dict

    return trs_contain


def convert_flows_to_df(flows_list: list):
    """
        Разворачивает список
    """

    df = pd.DataFrame([x for x in flows_list])

    df = df[[x for x in df.columns if x != '_id']]

    return df


def convert_flow_base_matrix_to_array(flows_list: list):
    """
        Разворачивает список
    """
    # ignore_keys = ['_id']
    # print('convert')
    _arr_contain = []
    for x in flows_list:
        try:
            its_code = first_or_none(list(x.keys()),
                                     lambda x: x != '_id' and x != 'version'and x != 'transport_type')
            _arr_contain.append(np.array(x[its_code]))
        except:
            continue

    res = np.array(_arr_contain)

    return res


def convert_dm_matrix_to_array(contain_list: list):
    """
        Разворачивает список
    """

    # print('convert')

    _arr_contain = []
    for x in contain_list:
        its_code = first_or_none(list(x.keys()),
                                 lambda x: x != '_id' and x != 'version' and x != 'transport_type')
        _arr_contain.append(np.array(x[its_code]))

    res = np.array(_arr_contain)

    return res


def convert_plos_express_info(plos_list: list):
    """
        Разворачивает список
    """

    plos_express_info_dict = {str(x['express_code']): {'geometry':
                                                       gload(x['geometry_wkt'])}
                              for x in plos_list
                              }

    return plos_express_info_dict


def convert_plos_avia_info(plos_list: list):
    """
        Разворачивает список
    """

    info_dict = {str(x['AIRPORT_ID']): {'geometry':
                                        gload(x['geometry']),
                                        'name_ru': x['NAME_RU']
                                        }
                 for x in plos_list
                 }

    return info_dict


def convert_elasticities_to_dict(el_list: list):
    df = pd.DataFrame(el_list)

    contain_dict = {}

    soc_types = df.soc_type.drop_duplicates().values

    for soc_type in soc_types:
        rec_soc = df[df['soc_type'] == soc_type]
        tr_types = rec_soc.transport_type.drop_duplicates().values
        soc_dict = {}
        for tr_type in tr_types:
            tr_dict = {}
            rec_tr = rec_soc[rec_soc['transport_type'] == tr_type]

            for x in rec_tr.itertuples():
                tr_dict[str(x.year)] = x.val
            soc_dict[tr_type] = tr_dict
        contain_dict[soc_type] = soc_dict
    return contain_dict

from data_loaders import ExcelLoader, CSVLoader, MongoLoader
from converters.converter_for_mongo import convert_mos_list_to_df
from converters.converter_for_mongo import convert_trs_to_valid_format
from converters.converter_for_mongo import convert_flows_to_df
from converters.converter_for_mongo import convert_plos_express_info
from converters.converter_for_mongo import convert_flow_base_matrix_to_array
from converters.converter_for_mongo import convert_dm_matrix_to_array
from converters.converter_for_mongo import convert_plos_avia_info
from converters.converter_for_mongo import convert_elasticities_to_dict

defaults = {
    'db_configs': {
        'postgres': {
            'engine': 'postgresql',
            'driver': 'psycopg2',
            'user': 'postgres',
            'password': '456rtyfgh',
            'host': 'localhost',
            'database': 'rounet_loko',
            'charset': 'utf8'
        },
        'mongo': {
            'host': 'localhost',
            'database': 'rounet_db',
            'port': 27017
        },
    },
    'loaders': [ExcelLoader, CSVLoader, MongoLoader],
    'source_list': ['Excel', 'QGSLayers', 'mongo'],
    'reg_transport_types': ['rail', 'avia'],
    'dataset_load_convert_func': {
        'mun_soc': convert_mos_list_to_df,
        'trs': convert_trs_to_valid_format,
        'flows_rail': convert_flows_to_df,
        'flows_avia': convert_flows_to_df,
        'plos_express_info': convert_plos_express_info,
        'plos_avia': convert_plos_avia_info,
        'flow_base_matrix': convert_flow_base_matrix_to_array,
        'dist_matrix': convert_dm_matrix_to_array,
        'elasticities': convert_elasticities_to_dict}

}


import math
from functools import partial

import numpy as np

import pyproj
from pyproj import Proj
from shapely.geometry import shape
from shapely.ops import transform


def first_or_none(i, func):
    try:
        return next(filter(func, i))

    except StopIteration:
        return None


def get_orthodromy(llat1, llong1, llat2, llong2):
    rad = 6372795

    lat1 = llat1 * math.pi / 180.
    lat2 = llat2 * math.pi / 180.
    long1 = llong1 * math.pi / 180.
    long2 = llong2 * math.pi / 180.

    # косинусы и синусы широт и разницы долгот
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    # вычисления длины большого круга
    y = math.sqrt(
        math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2)
    )
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = math.atan2(y, x)
    dist = ad * rad / 1000

    return dist


def row_orthodromy(lats: np.array, longs: np.array) -> np.array:
    """Finds a matrix of orthodromies of all points in a row

    You can access the resulting distances by indexes of every point
    i.e. distances[1][5] returns a distances (in meters) from first to
    fifth point

    Returns
    -------
    distances : 2-d np.array
        matrix of distances from each point to the others
    """

    lats = lats * np.pi / 180
    # 1d array
    longs = longs * np.pi / 180
    # 1d array

    # 1d array
    cosinuses = np.cos(lats)
    # 1d array
    sinuses = np.sin(lats)

    # 2d array
    delta = longs - longs[:, np.newaxis]
    # 2d array
    cdelta = np.cos(delta)
    # 2d array
    sdelta = np.sin(delta)

    # 2d array
    cos_sin = cosinuses * sinuses[:, np.newaxis]
    # 2d array
    sin_cos_cdelta = sinuses * cosinuses[:, np.newaxis] * cdelta
    # 2d array
    cos_sdelta = cosinuses * sdelta

    # 2d array
    y = np.sqrt(
        np.power(cos_sdelta, 2) +
        np.power(cos_sin - sin_cos_cdelta, 2)
    )
    # 2d array
    x = sinuses * sinuses[:, np.newaxis] + \
        cosinuses * cosinuses[:, np.newaxis] * cdelta

    ad = np.arctan2(y, x)

    rad = 6372795

    distances = ad * rad / 1000
    res_dm = np.zeros((distances.shape[0],
                       distances.shape[1]), dtype=float)
    for i in range(distances.shape[0]):
        for j in range(distances.shape[1]):
            average_dist = (distances[i][j] + distances[j][i])/2
            res_dm[i][j] = average_dist
            res_dm[j][i] = average_dist

    return res_dm


def convert_coord(crs_source, crs_target, x, y):
    """Converts single point to another crs
    """

    x2, y2 = pyproj.transform(
        pyproj.Proj(init=f'epsg:{crs_source}'),  # source coordinate system
        # destination coordinate system
        pyproj.Proj(init=f'epsg:{crs_target}'),
        x,
        y
    )

    return x2, y2


def convert_geometry(crs_source, crs_target, geometry):
    """Converts whole geometry to another crs
    """
    project = partial(
        pyproj.transform,
        pyproj.Proj(init=f'epsg:{crs_source}'),  # source coordinate system
        # destination coordinate system
        pyproj.Proj(init=f'epsg:{crs_target}'),
    )

    return transform(project, geometry)  # apply projection


def calc_deviation(target_vector_row,
                   target_vector_col,
                   gm):
    """
        Считает среднее квадратичное отклонение по строкам и по столбцам
    """
    #   среднее квадратичное отклонение по строкам
    sdr = np.power(target_vector_row - np.sum(gm, axis=1), 2)
    #   среднее квадратичное отклонение по строкам
    sdс = np.power(target_vector_col - np.sum(gm, axis=0), 2)

    return np.sum(sdr), np.sum(sdс)

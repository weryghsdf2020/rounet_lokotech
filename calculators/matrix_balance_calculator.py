import numpy as np
import pandas as pd


from utils import calc_deviation


class Fratar():
    def __init__(self,
                 target_vector_row,
                 target_vector_col,
                 matrix,
                 MAX_ITER=100,
                 LIMIT=0.0001):

        self.matrix = matrix
        self.rows = target_vector_row
        self.columns = target_vector_col

        self.MAX_ITER = MAX_ITER
        self.LIMIT = LIMIT
        self.gap = None

    def fit(self):
        start_deviation = calc_deviation(self.rows,
                                         self.columns,
                                         self.matrix)

        print(
            f'Стартовое среднее квадратичное отклонение по строкам: {start_deviation[0]}')
        print(
            f'Стартовое среднее квадратичное отклонение по столбцам: {start_deviation[1]}')

        rows = self.rows
        columns = self.columns

        self.gap = self.LIMIT + 1
        iter_count = 0

        while self.gap > self.LIMIT and iter_count < self.MAX_ITER:
            # print(1, self.gap)

            iter_count += 1

            marg_rows = self.tot_rows(self.matrix)
            row_factor = self.factor(marg_rows, rows)
            row_factor = np.nan_to_num(row_factor)

            self.matrix = np.transpose(
                np.transpose(self.matrix) * np.transpose(row_factor)
            )

            marg_cols = self.tot_columns(self.matrix)
            column_factor = self.factor(marg_cols, columns)
            column_factor = np.nan_to_num(column_factor)

            self.matrix = self.matrix * column_factor
            self.matrix = np.nan_to_num(self.matrix)

            self.gap = max(
                abs(1 - np.min(row_factor)),
                abs(np.max(row_factor) - 1),
                abs(1 - np.min(column_factor)),
                abs(np.max(column_factor) - 1),
            )
            # print(2, self.gap)

        final_deviation = calc_deviation(self.rows,
                                         self.columns,
                                         self.matrix)

        print(
            f'Итоговое среднее квадратичная отклонение по строкам: {final_deviation[0]}')
        print(
            f'Итоговое среднее квадратичная отклонение по столбцам: {final_deviation[1]}')

    def tot_rows(self, matrix):
        return np.nansum(matrix, axis=1)

    def tot_columns(self, matrix):
        return np.nansum(matrix, axis=0)

    def factor(self, marginals, targets):
        f = np.divide(targets, marginals)
        f[f == np.NINF] = 1
        return f

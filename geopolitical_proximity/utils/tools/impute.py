import pandas as pd
import numpy as np
from typing import Union, Optional
import warnings
from sklearn.impute import KNNImputer

warnings.filterwarnings("ignore")


class Imputer:

    def __init__(self, group_by_col: str) -> None:
        self.group_by_col = group_by_col

    def interpolate_values(
        self, dataframe: pd.DataFrame, max_consec: Optional[int] = None
    ) -> pd.DataFrame:
        return (
            dataframe.groupby(self.group_by_col)
            .apply(
                lambda group: group.interpolate(
                    method="index", limit_area="inside", limit=max_consec
                )
            )
            .reset_index(drop=True)
        )

    @staticmethod
    def limit_consec_values(
        values: list[Union[int, float]], max_consec: int, increment: int = 1
    ) -> list[Union[int, float]]:
        max_consec_vals = []
        n_consec = 0

        for i, x in enumerate(values):
            if i == 0:
                max_consec_vals.append(x)
                continue
            is_consec = x - values[i - 1] == increment
            n_consec = (n_consec + 1) if is_consec else 0
            if n_consec < max_consec:
                max_consec_vals.append(x)
        return max_consec_vals

    def extrapolate_values(
        self,
        dataframe: pd.DataFrame,
        x_col: str,
        y_col: str,
        max_consec: Optional[int] = None,
        increment: int = 1,
        floor: Optional[int] = None,
        ceiling: Optional[int] = None,
    ) -> list[Union[int, float]]:
        extrapolated_df = dataframe.copy()
        for group in extrapolated_df[self.group_by_col].unique():
            has_missing = extrapolated_df[y_col].isna()
            of_group = extrapolated_df[self.group_by_col] == group
            complete_data = (~has_missing) & (of_group)
            if len(extrapolated_df[complete_data]) < 2:
                continue
            x = extrapolated_df.loc[complete_data, x_col]
            y = extrapolated_df.loc[complete_data, y_col]
            x_pred = extrapolated_df.loc[(has_missing) & (of_group), x_col]
            if max_consec:
                x_pred = self.limit_consec_values(x_pred, max_consec, increment)
            coeff, intercept = np.polyfit(x, y, 1)
            extrapolated_df.loc[
                (extrapolated_df[x_col].isin(x_pred)) & (of_group), y_col
            ] = list(map(lambda x: intercept + coeff * x, x_pred))
        if ceiling is not None:
            extrapolated_df.loc[extrapolated_df[y_col] > ceiling, y_col] = ceiling
        if floor is not None:
            extrapolated_df.loc[extrapolated_df[y_col] < floor, y_col] = floor
        return extrapolated_df[y_col].tolist()

    def carry_values(
        self,
        dataframe: pd.DataFrame,
        value_col: str,
        max_consec: int = 5,
        forwards: bool = True,
        backwards: bool = True,
    ) -> list[Union[int, float]]:
        carried_values_df = dataframe.copy()
        if forwards:
            carried_values_df[value_col] = carried_values_df.groupby(self.group_by_col)[
                value_col
            ].ffill(limit=max_consec)
        if backwards:
            carried_values_df[value_col] = carried_values_df.groupby(self.group_by_col)[
                value_col
            ].bfill(limit=max_consec)
        return carried_values_df[value_col].tolist()

    def pct_completeness_by_group(
        self, dataframe: pd.DataFrame, value_col: str
    ) -> pd.DataFrame:
        return dataframe.groupby(self.group_by_col, as_index=False)[value_col].agg(
            {"complete_pct": lambda x: round(x.count() / x.size, 2)}
        )

    def impute_with_knn(
        self, dataframe: pd.DataFrame, value_col: str, cols_for_imputation: list[str]
    ) -> list[Union[int, float]]:
        knn_imputer = KNNImputer()
        all_cols = [value_col] + cols_for_imputation
        knn_imputed_values = knn_imputer.fit_transform(dataframe[all_cols])
        return [row[0] for row in knn_imputed_values]

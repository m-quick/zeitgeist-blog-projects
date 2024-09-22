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
        x: list[Union[int, float]], y: list[Union[int, float]], max_consec: int
    ) -> list[Union[int, float]]:

        missing_vals = [i for i, val in enumerate(y) if pd.isna(val)]
        missing_in_range = [
            val
            for val in missing_vals
            if any(
                [
                    not pd.isna(y[max(0, val - gap)])
                    or not pd.isna(y[min(val + gap, len(y) - 1)])
                    for gap in range(1, max_consec + 1)
                ]
            )
        ]
        return [x[i] for i in missing_in_range]

    def extrapolate_values(
        self,
        dataframe: pd.DataFrame,
        x_col: str,
        y_col: str,
        max_consec: Optional[int] = None,
        floor: Optional[int] = None,
        ceiling: Optional[int] = None,
    ) -> list[Union[int, float]]:
        extrapolated_df = dataframe.copy()
        if not max_consec:
            max_consec = len(extrapolated_df[x_col].unique()) - 2
        for group in extrapolated_df[self.group_by_col].unique():
            of_group = extrapolated_df[self.group_by_col] == group
            complete_data = (extrapolated_df[y_col].notna()) & (of_group)
            if len(extrapolated_df[complete_data]) < 2:
                continue
            x_train = extrapolated_df.loc[complete_data, x_col]
            y_train = extrapolated_df.loc[complete_data, y_col]
            x_total = extrapolated_df.loc[of_group, x_col].tolist()
            y_total = extrapolated_df.loc[of_group, y_col].tolist()
            x_pred = self.limit_consec_values(x_total, y_total, max_consec)
            coeff, intercept = np.polyfit(x_train, y_train, 1)
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

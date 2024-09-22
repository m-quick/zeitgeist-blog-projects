from datetime import datetime
import pandas as pd
import numpy as np
import requests
from typing import Optional, Callable
from bq.bq_tables import node_data
from utils.tools import BQConnector
from utils.types.variables import Variable


class WBDataHandler:

    def __init__(self, variable: Variable) -> None:
        self.bq = BQConnector()
        self.variable = variable

    def get_data(
        self,
        indicator_code: str,
        from_year: int,
        to_year: int,
        countries: Optional[list[str]] = None,
    ) -> pd.DataFrame:
        countries_str = ", ".join(countries) if countries else "all"
        url = f"https://api.worldbank.org/v2/country/{countries_str}/indicator/{indicator_code}"
        has_data = True
        page = 1
        params = {
            "per_page": 1_000,
            "format": "json",
            "date": f"{from_year}:{to_year}",
            "page": page,
        }
        indicator_data = []
        while has_data:
            response = requests.get(url, params=params)
            if not response.status_code == 200:
                raise Exception(f"Invalid response: {response.text}")
            data = response.json()
            has_data = data[1]
            indicator_data.extend(data[1])
            page += 1
            params.update({"page": page})

        dataframe = pd.DataFrame(indicator_data)
        dataframe = dataframe[["countryiso3code", "date", "value"]]
        dataframe["date"] = dataframe["date"].astype(int)
        dataframe = dataframe.sort_values(["countryiso3code", "date"], ascending=True)
        dataframe.loc[dataframe["value"].notna(), "is_imputed"] = False
        return dataframe

    def keep_nodes_only(self, raw_indicator_df: pd.DataFrame) -> pd.DataFrame:
        node_ids = self.bq.get_node_ids()
        return raw_indicator_df.merge(
            node_ids, left_on="countryiso3code", right_on="iso3", how="right"
        ).drop("countryiso3code", axis=1)

    def normalise_values(
        self,
        dataframe: pd.DataFrame,
        group_by_col: str,
        raw_values_col: str,
        apply_log: bool = True,
        log_function: Callable[[float], float] = np.log1p,
    ) -> list[float]:
        normalised_df = dataframe.copy()
        if apply_log:
            normalised_df[raw_values_col] = normalised_df[raw_values_col].apply(
                log_function
            )
        return normalised_df.groupby(group_by_col)[raw_values_col].transform(
            lambda x: (x - x.mean()) / x.std()
        )

    def format_df_for_upload(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe.rename(
            columns={
                "date": "year",
            }
        ).assign(variable_id=self.variable.id, date_added=datetime.now())
        dataframe["is_latest"] = (
            dataframe["year"]
            .groupby(dataframe["node_id"])
            .transform(lambda x: x == max(x))
        )
        dataframe["is_imputed"] = dataframe["is_imputed"].fillna(True)
        dataframe = dataframe[[col.name for col in node_data.columns]]
        return dataframe

    def upload_to_bq(self, dataframe: pd.DataFrame):
        return self.bq.upload_to_bq(dataframe, self.variable)

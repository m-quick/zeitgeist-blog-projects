from datetime import datetime
import pandas as pd
import numpy as np
import requests
from sklearn.preprocessing import StandardScaler
from typing import Optional, Callable, Union
from google.cloud.bigquery import Client
from settings import PROJECT
from bq.bq_tables import node_data, nodes, variables
from utils.types.variables import Variable


def add_col_combinations(dataframe: pd.DataFrame, index_cols: list[str]):
    if any([col not in dataframe.columns for col in index_cols]):
        raise IndexError("One or more index cols is missing form dataframe")
    index_cols_values = [dataframe[col].unique().tolist() for col in index_cols]
    multi_index = pd.MultiIndex.from_product(index_cols_values, names=index_cols)
    return dataframe.set_index(index_cols).reindex(multi_index).reset_index()


class WBDataHandler:

    def __init__(self, variable: Variable) -> None:
        self.bq = Client(PROJECT)
        self.variable = variable
        self.scaler = StandardScaler()

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

        indicator_df = pd.DataFrame(indicator_data)
        indicator_df = indicator_df[["countryiso3code", "date", "value"]]
        indicator_df["date"] = indicator_df["date"].astype(int)
        return indicator_df

    def get_node_ids(self) -> pd.DataFrame:
        job = self.bq.query(f"SELECT DISTINCT id AS node_id, iso3 FROM `{nodes.id}`")
        return job.result().to_dataframe()

    def keep_nodes_only(self, raw_indicator_df: pd.DataFrame) -> pd.DataFrame:
        node_ids = self.get_node_ids()
        return raw_indicator_df.merge(
            node_ids, left_on="countryiso3code", right_on="iso3", how="right"
        ).drop("countryiso3code", axis=1)

    def get_nodes_to_impute(
        self, indicators_df: pd.DataFrame, year_cutoff: int, get_rows: bool = False
    ) -> Union[int, pd.DataFrame]:
        none_recent_df = (
            indicators_df.loc[indicators_df["value"].notna()]
            .groupby("iso3", as_index=False)["date"]
            .max()
            .sort_values("date", ascending=True)
            .query(f"date < {year_cutoff}")
        )
        if get_rows:
            return none_recent_df
        return len(none_recent_df)

    def normalise_values(
        self,
        raw_values: pd.DataFrame,
        apply_log: bool = True,
        log_function: Callable[[float], float] = np.log1p,
    ) -> list[float]:
        if apply_log:
            raw_values = raw_values.apply(log_function)
        return self.scaler.fit_transform(raw_values)

    def format_df_for_upload(self, indicator_df: pd.DataFrame) -> pd.DataFrame:
        indicator_df = indicator_df.rename(
            columns={
                "date": "year",
            }
        ).assign(variable_id=self.variable.id, date_added=datetime.now())
        indicator_df["is_latest"] = (
            indicator_df["year"]
            .groupby(indicator_df["node_id"])
            .transform(lambda x: x == max(x))
        )
        indicator_df = indicator_df[[col.name for col in node_data.columns]]
        return indicator_df

    def upload_to_bq(self, indicators_df: pd.DataFrame) -> bool:
        data_uploaded = self.bq.load_table_from_dataframe(
            dataframe=indicators_df,
            destination=node_data.bq_table,
        )
        indicators_updated = self.bq.load_table_from_dataframe(
            dataframe=pd.DataFrame(
                {"id": self.variable.id, "name": self.variable.name}, index=[0]
            ),
            destination=variables.bq_table,
        )
        return data_uploaded.done() and indicators_updated.done()

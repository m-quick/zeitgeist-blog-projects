from datetime import datetime
import pandas as pd
import numpy as np
import requests
from typing import Optional, Callable
from google.cloud.bigquery import Client, LoadJob
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

    def get_node_ids(self) -> pd.DataFrame:
        job = self.bq.query(f"SELECT DISTINCT id AS node_id, iso3 FROM `{nodes.id}`")
        return job.result().to_dataframe()

    def keep_nodes_only(self, raw_indicator_df: pd.DataFrame) -> pd.DataFrame:
        node_ids = self.get_node_ids()
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

    def upload_to_bq(self, dataframe: pd.DataFrame) -> bool:
        jobs_status: list[LoadJob] = []
        data_uploaded = self.bq.load_table_from_dataframe(
            dataframe=dataframe,
            destination=node_data.bq_table,
        )
        jobs_status.append(data_uploaded)
        indicators_updated = self.bq.load_table_from_dataframe(
            dataframe=pd.DataFrame(
                {"id": self.variable.id, "name": self.variable.name}, index=[0]
            ),
            destination=variables.bq_table,
        )
        jobs_status.append(indicators_updated)
        return all([job.error_result is None for job in jobs_status])

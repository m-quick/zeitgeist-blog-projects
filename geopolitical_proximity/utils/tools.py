import pandas as pd
from google.cloud.bigquery import LoadJob, Client
from settings import PROJECT
from bq.bq_tables import variables, node_data, nodes
from utils.types.variables import Variable


def add_col_combinations(dataframe: pd.DataFrame, index_cols: list[str]):
    if any([col not in dataframe.columns for col in index_cols]):
        raise IndexError("One or more index cols is missing form dataframe")
    index_cols_values = [dataframe[col].unique().tolist() for col in index_cols]
    multi_index = pd.MultiIndex.from_product(index_cols_values, names=index_cols)
    return dataframe.set_index(index_cols).reindex(multi_index).reset_index()


class BQConnector:

    def __init__(self) -> None:
        self.bq = Client(PROJECT)

    def get_node_ids(self) -> pd.DataFrame:
        job = self.bq.query(f"SELECT DISTINCT id AS node_id, iso3 FROM `{nodes.id}`")
        return job.result().to_dataframe()

    def upload_to_bq(self, dataframe: pd.DataFrame, variable: Variable) -> bool:
        jobs_status: list[LoadJob] = []
        data_uploaded = self.bq.load_table_from_dataframe(
            dataframe=dataframe,
            destination=node_data.bq_table,
        )
        jobs_status.append(data_uploaded)
        indicators_updated = self.bq.load_table_from_dataframe(
            dataframe=pd.DataFrame(
                {"id": variable.id, "name": variable.name}, index=[0]
            ),
            destination=variables.bq_table,
        )
        jobs_status.append(indicators_updated)
        return all([job.error_result is None for job in jobs_status])

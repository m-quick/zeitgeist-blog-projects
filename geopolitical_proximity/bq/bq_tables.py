from dataclasses import dataclass
from datetime import datetime
from typing import Type

from bq.bq_datasets import Dataset, geopolitical_proximity
from bq.bq_types import BQ_TYPES
from google.cloud.bigquery import SchemaField
from google.cloud.bigquery import Table as BQTable
from settings import PROJECT


@dataclass
class Column:
    name: str
    field_type: Type
    mode: str = "REQUIRED"


@dataclass
class Table:
    dataset: Dataset
    name: str
    columns: list[Column]

    @property
    def id(self):
        return ".".join([PROJECT, self.dataset.name, self.name])

    @property
    def schema(self):
        return [
            SchemaField(col.name, BQ_TYPES[col.field_type], col.mode)
            for col in self.columns
        ]

    @property
    def bq_table(self):
        return BQTable(table_ref=self.id, schema=self.schema)


nodes = Table(
    dataset=geopolitical_proximity,
    name="nodes",
    columns=[
        Column("id", int),
        Column("name", str),
        Column("iso3", str),
        Column("type", str),
    ],
)

boundaries = Table(
    dataset=geopolitical_proximity,
    name="boundaries",
    columns=[Column("node_id", int), Column("geometry", str)],
)

node_data = Table(
    dataset=geopolitical_proximity,
    name="node_data",
    columns=[
        Column("node_id", int),
        Column("variable_id", int),
        Column("value", float, "NULLABLE"),
        Column("value_norm", float, "NULLABLE"),
        Column("is_imputed", bool),
        Column("is_latest", bool),
        Column("date_added", datetime),
        Column("year", int, "NULLABLE"),
    ],
)

variables = Table(
    dataset=geopolitical_proximity,
    name="variables",
    columns=[Column("id", int), Column("name", str)],
)

relationships_data = Table(
    dataset=geopolitical_proximity,
    name="relationships_data",
    columns=[
        Column("source_id", int),
        Column("target_id", int),
        Column("indicator_id", int),
        Column("value", float, "NULLABLE"),
        Column("value_norm", float, "NULLABLE"),
        Column("is_imputed", bool),
        Column("is_latest", bool),
        Column("date_updated", datetime),
        Column("year", int, "NULLABLE"),
    ],
)

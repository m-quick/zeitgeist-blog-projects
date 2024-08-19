from dataclasses import dataclass
from bq.bq_datasets import Dataset, geopolitical_proximity
from google.cloud.bigquery import SchemaField
from typing import Type
from bq.bq_types import BQ_TYPES
from settings import PROJECT
from shapely import Polygon
from datetime import datetime


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


nodes = Table(
    dataset=geopolitical_proximity,
    name="nodes",
    columns=[Column("id", int), Column("name", str), Column("type", str)],
)

boundaries = Table(
    dataset=geopolitical_proximity,
    name="boundaries",
    columns=[Column("node_id", int), Column("geometry", Polygon)],
)

node_data = Table(
    dataset=geopolitical_proximity,
    name="node_data",
    columns=[
        Column("node_id", int),
        Column("indicator_id", int),
        Column("value", float),
        Column("value_norm", float),
        Column("is_latest", bool),
        Column("date_updated", datetime),
        Column("year", int, "NULLABLE"),
    ],
)

indicators = Table(
    dataset=geopolitical_proximity,
    name="indicators",
    columns=[Column("id", int), Column("name", str), Column("type", str)],
)

connections_data = Table(
    dataset=geopolitical_proximity,
    name="connections_data",
    columns=[
        Column("source_id", int),
        Column("target_id", int),
        Column("indicator_id", int),
        Column("value", float),
        Column("value_norm", float),
        Column("is_latest", bool),
        Column("date_updated", datetime),
        Column("year", int, "NULLABLE"),
    ],
)
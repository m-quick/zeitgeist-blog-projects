from datetime import date, datetime
from shapely import Polygon

BQ_TYPES = {
    bool: "BOOL",
    int: "INT64",
    float: "FLOAT64",
    date: "DATE",
    datetime: "DATETIME",
    str: "STRING",
    Polygon: "GEOGRAPHY",
}

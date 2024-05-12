from typing import Union
from words_deeds.types.indicators import Indicator


def assign_dem_score(value: Union[int, float], indicator: Indicator) -> int:
    if value in indicator.more_dem:
        return 1
    elif value in indicator.less_dem:
        return -1
    return 0


def get_exec_suffixes(col_names: list[str]) -> list[str]:
    hos_indicators = [
        col.replace("hos", "") for col in col_names if col.startswith("hos")
    ]
    hog_indicators = [
        col.replace("hog", "") for col in col_names if col.startswith("hog")
    ]
    return [indicator for indicator in hos_indicators if indicator in hog_indicators]


def assign_exec_score(row: dict[str, int], exec_indicator: str) -> int:
    hos_val, hog_val = row[f"hos{exec_indicator}"], row[f"hog{exec_indicator}"]
    if hog_val == 1 or hos_val == 1:
        return 1
    elif hog_val == -1 or hos_val == -1:
        return -1
    return 0


def all_zero(row):
    return all([v == 0 for v in row.values])

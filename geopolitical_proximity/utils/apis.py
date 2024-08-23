import requests
import pandas as pd
from typing import Optional


def get_world_bank_data(
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
    return indicator_df

import pandas as pd


def add_col_combinations(dataframe: pd.DataFrame, index_cols: list[str]):
    if any([col not in dataframe.columns for col in index_cols]):
        raise IndexError("One or more index cols is missing form dataframe")
    index_cols_values = [dataframe[col].unique().tolist() for col in index_cols]
    multi_index = pd.MultiIndex.from_product(index_cols_values, names=index_cols)
    return dataframe.set_index(index_cols).reindex(multi_index).reset_index()

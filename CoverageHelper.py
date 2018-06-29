import pandas as pd


def filter(type: str, strategy: str, df: pd.DataFrame):
    return df[(df.coverage_type == type) & (df.strategy == strategy)]

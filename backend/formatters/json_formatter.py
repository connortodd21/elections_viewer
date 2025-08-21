import pandas as pd

def dfToJson(df: pd.DataFrame) -> dict:
    return df.to_json(orient="records")
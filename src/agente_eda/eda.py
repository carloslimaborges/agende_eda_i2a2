import numpy as np, pandas as pd

def compact_overview(df: pd.DataFrame, sample_rows: int=10, max_unique_preview: int=10) -> dict:
    schema = [{"name": c, "dtype": str(df[c].dtype)} for c in df.columns]
    sample = df.head(sample_rows).fillna("∅").astype(str).to_dict(orient="records")
    return {"rows": len(df), "cols": len(df.columns), "schema": schema, "sample": sample}

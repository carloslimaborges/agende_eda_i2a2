import pandas as pd, numpy as np

def generate_insights(df: pd.DataFrame, limit: int=5) -> str:
    lines = []
    num = df.select_dtypes(include=[np.number])
    if not num.empty:
        variances = num.var().sort_values(ascending=False)
        top = variances.index[:3].tolist()
        if len(top)>0: lines.append(f"Maior variabilidade em: {', '.join(top)}.")
    return " ".join(lines[:limit]) if lines else "Sem insights automáticos relevantes."

import pandas as pd

def load_csv(file, sep=",", decimal=".", encoding="utf-8"):
    return pd.read_csv(file, sep=sep, decimal=decimal, encoding=encoding, low_memory=False)

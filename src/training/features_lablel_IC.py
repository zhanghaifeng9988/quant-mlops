import pandas as pd
import numpy as np 
from pathlib import Path
PROCESSED_DIR = Path("data/features")

FEATURE_COLS = [
    "ret_1d", "ret_5d", "ret_20d",
    "vol_5d", "vol_20d",
    "vol_ratio", "price_pos", "ma_ratio",
]

df = pd.read_parquet(PROCESSED_DIR / "features.parquet")

def main():
    for f in FEATURE_COLS:
        ic = df.groupby("date").apply(lambda g: g[f].corr(g["label"])).mean()
        print(f"{f:>12}: IC = {ic:+.4f}")

if __name__ == "__main__":
    main()
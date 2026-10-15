from pathlib import Path
import pandas as pd
import numpy as np

# 把清洗后的价格数据（prices.parquet）
# 加工成带技术指标 + 预测标签的数据集（features.parquet），供后续机器学习使用。

PROCESSED_DIR = Path("data/processed")
FEATURES_DIR = Path("data/features")

# 特征创建，就是X值
def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["ticker", "date"]).copy() # 按 ticker 和 date 排序
    g = df.groupby("ticker", group_keys=False) # 按 ticker 分组,让分组操作不额外加一层索引，输出更干净。

    # 动量特征
    df["ret_1d"] = g["close"].pct_change(1)
    df["ret_5d"] = g["close"].pct_change(5)
    df["ret_20d"] = g["close"].pct_change(20)

    # 波动率特征
    df["vol_5d"] = g["ret_1d"].transform(lambda x: x.rolling(5).std())
    df["vol_20d"] = g["ret_1d"].transform(lambda x: x.rolling(20).std())

    # 成交量强度,量价特征
    df["vol_ma20"] = g["volume"].transform(lambda x: x.rolling(20).mean()) # 20 日成交量移动平均
    df["vol_ratio"] = df["volume"] / df["vol_ma20"]  # 当日成交量/20日均量 ，成交量强度。> 1 表示放量，< 1 表示缩量

    # 价格位置（当前收盘价在 20 日高低区间的位置），衡量价格在近期区间中的相对位置
    df["high_20"] = g["high"].transform(lambda x: x.rolling(20).max())
    df["low_20"] = g["low"].transform(lambda x: x.rolling(20).min())
    df["price_pos"] = (df["close"] - df["low_20"]) / (df["high_20"] - df["low_20"])

    # 均线比率，趋势特征
    df["ma_5"] = g["close"].transform(lambda x: x.rolling(5).mean())
    df["ma_20"] = g["close"].transform(lambda x: x.rolling(20).mean())
    df["ma_ratio"] = df["ma_5"] / df["ma_20"]

    return df

# 添加预测标签，就是y值
def add_label(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["ticker", "date"]).copy()
    g = df.groupby("ticker", group_keys=False)
    # label 在 t 时刻 = (close[t+1] / close[t]) - 1，用 shift(-1) 对齐到 t
    df["label"] = g["close"].pct_change(1).shift(-1)
    return df


def main():
    FEATURES_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet(PROCESSED_DIR / "prices.parquet")
    df = compute_features(df)
    df = add_label(df)

    feature_cols = [
        "ret_1d", "ret_5d", "ret_20d",
        "vol_5d", "vol_20d",
        "vol_ratio", "price_pos", "ma_ratio",
    ]

    # 去掉窗口不足和 label 缺失的行
    before = len(df)
    df = df.dropna(subset=feature_cols + ["label"]).reset_index(drop=True) # 删掉有nan值的行，重建索引，丢弃原索引值
    after = len(df)
    print(f"dropped {before - after} rows (warmup + label NaN), kept {after}")

# 保存特征数据集，含y值
    out = FEATURES_DIR / "features.parquet"
    df.to_parquet(out, index=False) # index=False 的意思是：保存 parquet 文件时，不要把 DataFrame 的索引写进去。
    print(f"saved -> {out}")
    print(f"date range: {df['date'].min().date()} ~ {df['date'].max().date()}")
    print(f"features: {feature_cols}")


if __name__ == "__main__":
    main()
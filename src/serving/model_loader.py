# src/serving/model_loader.py
# 模型加载模块

from pathlib import Path
from functools import lru_cache  # 这是装饰器，用来缓存函数的返回值
import mlflow
import mlflow.pyfunc
import pandas as pd

MODEL_NAME = "us-stock-lgbm-1d"
MODEL_ALIAS = "candidate"
TRACKING_URI = "sqlite:///mlflow.db"
FEATURES_PATH = Path("data/features/features.parquet")

FEATURE_COLS = [
    "ret_1d", "ret_5d", "ret_20d",
    "vol_5d", "vol_20d",
    "vol_ratio", "price_pos", "ma_ratio",
]

# 加载模型，maxsize=1只存 1 个结果
@lru_cache(maxsize=1)
def load_model():
    mlflow.set_tracking_uri(TRACKING_URI)
    uri = f"models:/{MODEL_NAME}@{MODEL_ALIAS}"
    model = mlflow.pyfunc.load_model(uri)
    return model

# 加载特征
@lru_cache(maxsize=1)
def load_features():
    df = pd.read_parquet(FEATURES_PATH)
    df["date"] = pd.to_datetime(df["date"])
    return df
# src/serving/app.py
# 把异步生成器函数变成异步上下文管理器，用来定义 FastAPI 的生命周期事件（启动/关闭时执行什么）。
from contextlib import asynccontextmanager 

from fastapi import FastAPI, HTTPException
import pandas as pd

from src.serving.model_loader import (
    load_model, load_features,
    MODEL_NAME, MODEL_ALIAS, FEATURE_COLS,
)
from src.serving.schemas import (
    PredictRequest, PredictResponse,
    HealthResponse, ModelInfoResponse,
)

# FastAPI 推荐的生命周期写法
# 装饰器，让这个异步函数支持 yield 前后分别执行代码。
@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    load_features()
    #yield — 分隔点。yield 之前的代码在启动时跑，yield 之后的代码在服务关闭时跑
    # #（这里没写，所以关闭时不做清理）。
    yield
# 为什么这样做？ 模型加载很慢，不能每次请求都加载。放到启动时执行一次，之后所有请求复用内存中的模型。


# 创建 FastAPI 应用实例,title — 显示在自动生成的 API 文档（Swagger UI）标题上。
# lifespan=lifespan — 把上面定义的生命周期函数挂到应用上。
app = FastAPI(title="Quant MLOps Serving", lifespan=lifespan)


@app.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok"}


@app.get("/model/info", response_model=ModelInfoResponse)
def model_info():
    df = load_features()
    return {
        "model_name": MODEL_NAME,
        "alias": MODEL_ALIAS,
        "feature_count": len(FEATURE_COLS),
        "n_rows_loaded": len(df),
    }


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    df = load_features()
    target_date = pd.to_datetime(req.date)

    row = df[(df["ticker"] == req.ticker) & (df["date"] == target_date)]
    if row.empty:
        raise HTTPException(
            status_code=404,
            detail=f"no features for {req.ticker} on {req.date}",
        )

    features = row[FEATURE_COLS]
    pred = load_model().predict(features)
    
    return {
        "ticker": req.ticker,
        "date": req.date,
        "prediction": float(pred[0]),
        "model_name": MODEL_NAME,
        "model_alias": MODEL_ALIAS,
    }
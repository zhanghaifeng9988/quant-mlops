# src/serving/schemas.py
# 这段代码是用 Pydantic 定义的几个数据模型（BaseModel）
# 用来定义 API 的请求体和响应体结构。
from pydantic import BaseModel

#定义预测请求的结构
class PredictRequest(BaseModel):
    ticker: str
    date: str  # YYYY-MM-DD

# 定义预测响应的结构
class PredictResponse(BaseModel):
    ticker: str
    date: str
    prediction: float
    model_name: str
    model_alias: str

#定义健康检查响应的结构
class HealthResponse(BaseModel):
    status: str

#定义模型信息响应的结构
class ModelInfoResponse(BaseModel):
    model_name: str
    alias: str
    feature_count: int
    n_rows_loaded: int
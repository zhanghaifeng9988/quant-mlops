# PROJECT CONTEXT

> 每次新开对话，先把这个文件内容贴给 AI，说“继续”。

## 项目定位

**MLOps Pipeline for Financial Time Series Prediction**
- 以美股预测为业务载荷的端到端 MLOps 系统
- 核心是展示 MLOps 工程能力，量化只是背景

## 仓库信息

- 远程仓库：`https://github.com/zhanghaifeng9988/quant-mlops.git`（GitHub）
- 本地路径：`/home/mlops/quant-mlops-project`
- GitHub Description：`End-to-end MLOps system for financial time series prediction...`

## 技术栈

- 环境：uv（pyproject.toml + uv.lock），Python 3.11
- 数据：yfinance，Parquet
- 特征/训练：pandas, LightGBM, scikit-learn
- 实验追踪：MLflow（sqlite 后端 `sqlite:///mlflow.db`，artifact 在 `mlruns/`）
- 服务：FastAPI + uvicorn
- 容器：Docker，即将用 docker-compose
- 监控（进行中）：PostgreSQL 18 + Grafana 11.2
- 编排：Prefect（阶段二后用）
- 阶段三：Kubernetes (kind/minikube) + GitHub Actions

## 阶段进度

### 阶段一：端到端可复现实验 ✅

- 数据：S&P 100，2015-02 ~ 2026-09
- 特征：8 个因子（ret_1d/5d/20d, vol_5d/20d, vol_ratio, price_pos, ma_ratio）
- Point-in-time 正确（label[t] = ret_1d[t+1]）
- 5 折 walk-forward 训练
- 结果：test IC 0.0091±0.0056，RankIC 0.0112±0.0124，best_iter 1-23（信号弱）

### 阶段二：生产化闭环（进行中）

已完成：
1. ✅ 模型注册
   - 模型名：`us-stock-lgbm-1d`
   - v2 = fold 1，alias `champion`
   - v3 = fold 5，alias `candidate`
   - 服务端加载 `@candidate`（fold 5）
2. ✅ FastAPI 服务
   - `/health`, `/model/info`, `/predict`
   - 代码：`src/serving/app.py`, `model_loader.py`, `schemas.py`
3. ✅ Docker 化
   - `Dockerfile`：基于 `python:3.11.16-slim-bookworm`
   - WORKDIR 与宿主机一致：`/home/mlops/quant-mlops-project`（MLflow db 里写死了路径）
   - 镜像：`quant-mlops-serving:v1`
   - `.dockerignore` 已配置
4. 🔄 Docker Compose 统一管理
   - 计划整合：serving + postgres + grafana
   - 文件：`docker-compose.yml`, `init-db/init.sql`

未完成：
5. 监控与漂移检测（4 类指标）
6. 自动重训练（Prefect）

### 阶段三：K8s + CI/CD（待做）

### 阶段四：平台能力扩展（待做）
- 特征库（Feast）
- 策略回测支撑
- 另类数据实验

## 监控设计（当前讨论定稿）

### 四类指标
1. 服务健康：QPS、p95 延迟、5xx 率
2. 模型性能：滚动 IC/RankIC、RMSE、方向准确率
3. 数据质量：NaN 率、越界率、缺失
4. 数据漂移 + 概念漂移：特征 PSI/KS、预测-标签关系变化

### 架构
FastAPI → PostgreSQL（predictions/labels/drift_metrics/service_logs）→ Grafana
↑
Prefect job（跑 Evidently）



### 4 张表（见 init-db/init.sql）
- `predictions`：含 client_ip, client_version
- `labels`
- `drift_metrics`
- `service_logs`：含 client_ip, client_version

### 分阶段执行
1. 服务健康 → 2. 数据质量 + 数据漂移 → 3. 模型性能 + 概念漂移 → 4. 自动重训练

## 关键决策记录

- 不用 stage，用 alias（MLflow 2.9+ 已废弃 stage）
- `log_model(name="model")` 返回的 `model_info.model_uri` 存 tag，注册时读 tag，不拼路径
- `batch_id` 区分多次训练的 fold 重复问题
- 服务端预加载 features.parquet，按 ticker+date 查表（保证 training-serving 一致）
- 镜像基础用 `slim-bookworm` + apt 装 `libgomp1`（LightGBM 依赖）
- Docker WORKDIR 与宿主机对齐（MLflow artifact 路径问题）

## 常用命令

```bash
# 本地开发
uv run python -m src.data.download
uv run python -m src.data.build_processed
uv run python -m src.features.build_features
uv run python -m src.training.train
uv run python -m src.registry.register --run-id <id> --alias candidate

# 本地服务
uv run uvicorn src.serving.app:app --reload --port 8000

# MLflow UI
uv run mlflow ui --backend-store-uri sqlite:///mlflow.db

# Docker
sudo docker build -t quant-mlops-serving:v1 .
sudo docker run -d --name quant-serving -p 8000:8000 quant-mlops-serving:v1
sudo docker compose up -d
sudo docker compose ps
sudo docker logs quant-serving



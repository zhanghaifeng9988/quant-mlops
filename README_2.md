# MLOps Pipeline for Financial Time Series Prediction

- 一个以股市预测为业务载荷的端到端 MLOps 系统。  
- 核心目标是展示 MLOps 工程能力：数据版本、实验追踪、模型注册、服务、监控、自动重训练、CI/CD。
- 量化是背景，MLOps 是主角。

## 技术栈

- 数据：akshare / yfinance，Parquet
- 特征与训练：pandas, scikit-learn, XGBoost/LightGBM
- 实验追踪：MLflow
- 编排：Prefect
- 服务：FastAPI / BentoML
- 监控：Evidently 或自写脚本
- 容器：Docker, Docker Compose
- 编排（后期）：Kubernetes (kind/minikube)
- CI/CD：GitHub Actions


## 三阶段路线图

### 阶段一：端到端可复现实验
从原始数据到模型评估，一条命令跑通全流程，MLflow 记录可对比实验。

### 阶段二：生产化闭环
模型注册、REST 服务、监控与漂移检测、自动重训练，docker-compose 一键拉起。

### 阶段三：K8s 部署 + CI/CD
将阶段二系统部署到本地 K8s，加入 GitHub Actions 自动化测试、构建与部署。


## 项目状态

- [ ] 阶段一：端到端可复现实验
- [ ] 阶段二：生产化闭环
- [ ] 阶段三：K8s 部署 + CI/CD



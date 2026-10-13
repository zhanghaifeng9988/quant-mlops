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

### 阶段四：平台能力扩展
特征库（Feast）、策略回测支撑、另类数据实验支持，让平台具备服务真实研究员的完整能力。

## 项目状态

- [√] 阶段一：端到端可复现实验
- [ ] 阶段二：生产化闭环
- [ ] 阶段三：K8s 部署 + CI/CD
- [ ] 阶段四：平台能力扩展

## 阶段一总结
### 已完成：
- 数据：S&P 100，2015-2026，yfinance 下载 → parquet 存储 → 校验 → 合并
- 特征：8 个基础因子，point-in-time 正确（label[t] = ret_1d[t+1]）
- 训练：5 折 walk-forward，LightGBM + early stopping
- 追踪：MLflow（sqlite 后端），每折记录参数、指标、模型、feature importance
- 环境：uv 管理，uv.lock 可复现
### 结果：
- test IC 0.0091 ± 0.0056，RankIC 0.0112 ± 0.0124
- best_iter 1-23，说明信号弱，但pipeline完整，评估体系可靠
- 结论：MLOps 骨架完整，策略信号弱是数据问题，不是工程问题
### 过程记录：
- quant-mlops-project/notebooks/01_env_data_clean.ipynb 
- quant-mlops-project/notebooks/02_feature_point_in_time.ipynb 
- quant-mlops-project/notebooks/03_split_training_mlfow.ipynb


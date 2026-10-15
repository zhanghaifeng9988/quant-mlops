# ROADMAP

> 规划是行动指南，不是承诺书。每阶段结束后迭代更新。

## 阶段一：端到端可复现实验 ✅

**完成定义**：clone 仓库后，一条命令跑通数据获取 → 特征 → 训练 → 评估，MLflow 中有可对比实验记录。

| 里程碑 | 产出 |
|--------|------|
| 1. 数据获取与存储 | S&P 100 日频数据，Parquet 存储 |
| 2. 特征工程 | 8 个基础因子，point-in-time 正确 |
| 3. 训练与实验追踪 | LightGBM，5 折 walk-forward，MLflow 记录 |
| 4. 评估 | IC/RankIC/feature importance |

**结果**：test IC 0.0091，RankIC 0.0112。

**难点**：数据泄漏处理、walk-forward、point-in-time 特征、best_iter 诊断。

---

## 阶段二：生产化闭环（进行中）

**完成定义**：docker-compose 拉起 MLflow + 模型服务 + 监控，模型可注册、可服务、可检测漂移、可自动重训练。

| 里程碑 | 产出 | 状态 |
|--------|------|------|
| 1. 模型注册 | MLflow Model Registry，alias 管理（champion=v2/fold1，candidate=v3/fold5） | ✅ |
| 2. 模型服务 | FastAPI REST API，/health /model/info /predict | ✅ |
| 3. Docker 化 | Dockerfile，镜像 quant-mlops-serving | ✅ |
| 4. Docker Compose 统一管理 | serving + postgres + grafana 一键拉起 | 进行中 |
| 5. 监控与漂移检测 | 4 类指标（服务健康/模型性能/数据质量/漂移），PG 存储 + Grafana 可视化 | 进行中 |
| 6. 自动重训练 | Prefect 定时触发，漂移超阈值自动重训练并评估替换 | 待做 |

**难点**：alias 管理模型生命周期、training-serving skew、容器化部署、4 类监控指标体系。


## 阶段三：K8s 部署 + CI/CD

**完成定义**：阶段二系统部署到本地 K8s，GitHub Actions 自动测试、构建镜像、部署。

| 里程碑 | 产出 |
|--------|------|
| 1. 本地 K8s | kind/minikube 集群，部署 MLflow、模型服务 |
| 2. K8s 配置 | Deployment, Service, Ingress, ConfigMap, Secret, PV, HPA |
| 3. CI/CD | GitHub Actions：push 后跑测试、构建镜像、部署 |

**难点**：K8s 资源配置、CI/CD 模型版本处理、规模扩大后的瓶颈。

---

## 阶段四：平台能力扩展

**完成定义**：平台具备特征库、策略回测支撑、另类数据实验能力，能支撑研究员的完整工作流。

| 里程碑 | 产出 |
|--------|------|
| 1. 特征库 | 引入 Feast，管理特征版本与训练/推理一致性 |
| 2. 策略回测支撑 | 最小回测链路：预测 → 选股 → 净值曲线，输出年化/夏普/回撤 |
| 3. 另类数据实验 | 公开另类数据（舆情/趋势）接入，验证平台的扩展能力 |

**难点**：training-serving skew 与 Feature Store、平台如何服务研究员、从预测到策略的闭环。

---

## 时间线（？h/天）

- 阶段一：已完成
- 阶段二：约 2-3 周
- 阶段三：约 1-2 周
- 阶段四：约 2-3 周
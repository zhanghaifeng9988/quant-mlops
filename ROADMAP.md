# ROADMAP

- 规划是行动指南，不是承诺书。每阶段结束后迭代更新。

## 阶段一：端到端可复现实验（约  个月）

**完成定义**：clone 仓库后，一条命令跑通数据获取 → 特征 → 训练 → 评估，MLflow 中有可对比实验记录。

| 里程碑 | 产出 |
|--------|------|
| 1. 数据获取与存储 | 日频数据下载脚本，Parquet 按日期分区，基础元数据记录 |
| 2. 特征工程 | 20-50 个基础因子，point-in-time 正确性处理 |
| 3. 训练与实验追踪 | XGBoost/LightGBM 训练，TimeSeriesSplit，MLflow 记录参数与指标 |
| 4. 评估与回测 | IC/RankIC/回测收益计算，结果可视化 |
| 5. Prefect 编排 | 全流程 Flow，参数化运行，支持定时调度 |

**可讲**：数据泄漏处理、TimeSeriesSplit、point-in-time 特征。

---

## 阶段二：生产化闭环（约  个月）

**完成定义**：docker-compose 拉起 MLflow + Prefect + 模型服务 + 监控，模型可注册、可服务、可检测漂移、可自动重训练。

| 里程碑 | 产出 |
|--------|------|
| 1. 模型注册 | MLflow Model Registry，Staging/Production 阶段管理 |
| 2. 模型服务 | FastAPI/BentoML REST API，Docker 化 |
| 3. 监控与漂移检测 | 预测分布、特征分布记录，Evidently 或自写脚本 |
| 4. 自动重训练 | Prefect 定时触发，漂移超阈值自动重训练并评估替换 |

**可讲**：漂移阈值定义、新模型上线决策、服务延迟压测。

---

## 阶段三：K8s 部署 + CI/CD（约  个月）

**完成定义**：阶段二系统部署到本地 K8s，GitHub Actions 自动测试、构建镜像、部署。

| 里程碑 | 产出 |
|--------|------|
| 1. 本地 K8s | kind/minikube 集群，部署 MLflow、Prefect worker、模型服务 |
| 2. K8s 配置 | Deployment, Service, Ingress, ConfigMap, Secret, PV, HPA |
| 3. CI/CD | GitHub Actions：push 后跑测试、构建镜像、部署 |

**可讲**：K8s 资源配置、CI/CD 模型版本处理、规模扩大后的瓶颈。

---

## 时间线（ 10h/天）

- 阶段一：第 1- 周
- 阶段二：第 - 周
- 阶段三：第 - 周
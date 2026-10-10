# 一、项目思考、思路、概述
# Quant ML Platform / QuantOps Platform  

## 1.概述
- 面向量化机器学习场景的 AI/ML Engineering Platform。
- 股票市场是业务场景，不是最终研究目标。

## 2.***核心目标***：
- 以量化交易作为业务场景，设计并开发一个能够支撑数据、实验、训练、模型管理、工作流编排、模型服务、监控以及后续 LLM 应用的 AI/ML 工程平台。
- 为量化投研团队构建一套工程化、自动化的机器学习研发与模型生命周期管理平台，帮助研究员将研究想法转化为可复现、可评估、可部署和可持续迭代的机器学习模型及策略原型。
- 量化MLOps的工作覆盖了模型从研发到上线的全生命周期，核心是搭建和维护一套可靠的工程化体系
- 量化MLOps的主要服务对象是量化研究员（Quantitative Researchers），他们是策略的“发明家”。MLOps 工程师主要负责将研究流程工程化、自动化和标准化，为研究员提供稳定的数据、实验、训练、模型管理、部署和监控能力，并与算法/研究及生产工程团队协作，将经过验证的研究成果转化为可维护、可运行的生产模型。
- 最典型的场景是自动化、高频次的策略迭代。例如，一家量化私募基金，其MLOps平台需要支持研究员每天处理全市场数据，计算上千个因子，训练预测次日收益的模型，并自动生成交易信号。MLOps的价值在于，它通过工程化手段将这个过程标准化、自动化，从而将策略从研发到上线的周期从数月缩短到数天。

## 3.股票市场只是我们的业务载荷。真正要展示的是：MLOps / LLMOps 平台工程能力。

## 4.项目框架思路，架构方向
┌────────────────────────────────────────────┐
│              QuantOps Platform             │
├────────────────────────────────────────────┤
│                                            │
│  Layer 4：LLMOps                           │
│  Prompt / LLM / Evaluation / Tracing       │
│                                            │
├────────────────────────────────────────────┤
│                                            │
│  Layer 3：MLOps                            │
│  Dataset / Experiment / Pipeline           │
│  Model Registry / Serving / Monitoring     │
│                                            │
├────────────────────────────────────────────┤
│                                            │
│  Layer 2：Application / Business           │
│  Quant Research / Prediction / Backtest    │
│                                            │
├────────────────────────────────────────────┤
│                                            │
│  Layer 1：Infrastructure                   │
│  DB / Object Storage / Docker / Network    │
│                                            │
└────────────────────────────────────────────┘
                         │
                   后期再引入 K8s

### 核心重点
Layer 3：MLOps

### 第二重点
Layer 4：LLMOps

### 业务载荷
Layer 2：Quant

### 基础支撑
Layer 1：Infrastructure

### 最后再研究
Kubernetes


### 闭环一：训练闭环
Data
 ↓
Feature
 ↓
Training
 ↓
Experiment
 ↓
Model

### 闭环二：生产闭环
Model
 ↓
Deployment
 ↓
Prediction
 ↓
Monitoring
 ↓
Drift


### 闭环三：迭代闭环
Monitoring
 ↓
发现问题
 ↓
Retraining
 ↓
New Model
 ↓
Evaluation
 ↓
Production


## 5. LLMOps 是怎么接进来的？

不是另起炉灶。

而是在 MLOps 平台上继续增加：
                   QuantOps
                      │
          ┌───────────┴───────────┐
          │                       │
        MLOps                   LLMOps
          │                       │
      ML Model                LLM Model
          │                       │
      Training                Prompt
          │                       │
      Evaluation              Evaluation
          │                       │
      Registry                Registry
          │                       │
      Deployment              Gateway
          │                       │
      Monitoring              Tracing


## 6.最终才是 Kubernetes

到那个时候，已经有：

QuantOps
├── MLOps
│   ├── Pipeline
│   ├── Model Registry
│   ├── Serving
│   └── Monitoring
│
└── LLMOps
    ├── Gateway
    ├── Prompt
    ├── Evaluation
    └── Tracing

- 如果我要让它运行在一个真正的生产环境怎么办？
- 这时 Kubernetes 才有意义。
- 学习：

Deployment
Service
Ingress
Job
CronJob
ConfigMap
Secret
PersistentVolume
HPA
GPU

- 每学一个都有实际的落点。

- 这时候 K8s 就不再是：“背 YAML。”

- 而是：解决我的 QuantOps 平台部署问题。

这个学习效率会高很多。

# 二、“总体共识”正式定成这样，以后围绕这个目标走：

## 1.项目目标：
构建一个以量化交易为业务场景、以 MLOps 为核心、逐步扩展至 LLMOps，并最终探索 Kubernetes 生产部署的 AI Engineering Platform。
- 以量化交易作为业务场景，设计并开发一个能够支撑数据、实验、训练、模型管理、工作流编排、模型服务、监控以及后续 LLM 应用的 AI/ML 工程平台。
- 是为量化投研团队构建一套工程化、自动化的**“策略生产流水线”*，让研究员能高效地将想法转化为稳定运行的交易策略。
- 量化MLOps的工作覆盖了模型从研发到上线的全生命周期，核心是搭建和维护一套可靠的工程化体系
- 量化MLOps的主要服务对象是量化研究员（Quantitative Researchers），他们是策略的“发明家”。MLOps工程师则作为“工程师”角色，与研究员和交易员紧密协作，将研究想法转化为实际的生产力。
- 最典型的场景是自动化、高频次的策略迭代。例如，一家量化私募基金，其MLOps平台需要支持研究员每天处理全市场数据，计算上千个因子，训练预测次日收益的模型，并自动生成交易信号。MLOps的价值在于，它通过工程化手段将这个过程标准化、自动化，从而将策略从研发到上线的周期从数月缩短到数天。
## 2.技术路线：
                    QuantOps
                       │
                       ↓
              ┌────────────────┐
              │     MLOps      │
              │    第一阶段     │
              └───────┬────────┘
                      ↓
              ┌────────────────┐
              │    LLMOps      │
              │    第二阶段     │
              └───────┬────────┘
                      ↓
              ┌────────────────┐
              │ Kubernetes     │
              │   第三阶段      │
              └────────────────┘


## 2. 不需要成为：

- 量化策略专家
- Alpha researcher
- 高频交易员
- 衍生品专家
- 量化交易员

但是你需要大致理解：

量化团队从想法到生产的全过程

可以先形成这么一张脑图：
                    Quant Team
                        │
             ┌──────────┴──────────┐
             │                     │
          Research              Engineering
             │                     │
             ↓                     ↓
         Market Data          Data Platform
             │                     │
             ↓                     ↓
        Feature/Factor        Data Pipeline
             │                     │
             ↓                     │
       Model / Strategy            │
             │                     │
             ↓                     │
          Backtest                 │
             │                     │
             ↓                     │
       Evaluation ◄───────────────┘
             │
             ↓
        Model / Strategy
             │
             ↓
         Production
             │
             ↓
        Monitoring
             │
             ↓
        Retraining

## 3.我们主要关注：

数据
 ↓
特征
 ↓
ML Dataset
 ↓
训练
 ↓
实验
 ↓
模型
 ↓
模型服务
 ↓
监控

## 4.我们最终真正要模拟的是这样一个小型量化团队

例如：

                  Quant Company
                       │
       ┌───────────────┼───────────────┐
       │               │               │
   Researcher       ML Engineer     Platform
       │               │               │
       │               │          QuantOps
       │               │               │
       ↓               ↓               ↓
    Strategy        Model          Infrastructure
    /Factor         Training        /Pipeline
       │               │               │
       └───────────────┼───────────────┘
                       ↓
                  Production

你在这个项目中的角色不是：Researcher。

也不是：Trader。

而是：ML Platform / MLOps Engineer  


## 5. 真正的 QuantOps 应该逐渐变成：

                  Market Data
                      │
                      ↓
              Data Validation
                      │
                      ↓
                Dataset Version
                      │
                      ↓
              Feature Pipeline
                      │
                      ↓
                Training Data
                      │
                      ↓
               Training Pipeline
                      │
             ┌────────┴────────┐
             ↓                 ↓
         Experiment         Evaluation
             │                 │
             └────────┬────────┘
                      ↓
                Model Registry
                      │
               ┌──────┴──────┐
               ↓             ↓
           Backtest       Model API
               │             │
               ↓             ↓
           Evaluation     Production
               │             │
               └──────┬──────┘
                      ↓
                  Monitoring
                      │
                      ↓
                 Retraining

这就已经很像一个真正的 ML Platform 了。


# Phase 0：Quant ML Research Experience
## 概述
在正式设计 QuantOps 平台之前，先暂时站在量化研究员的视角，亲自完成一个小型、完整的机器学习量化研究项目。

目标不是培养量化策略研究能力，也不是追求交易收益，而是：

- 理解量化研究员实际使用的数据；
- 理解从市场数据到特征、Label、Dataset 的过程；
- 亲自完成一次机器学习模型训练；
- 理解时间序列数据划分、数据泄漏、回测等关键问题；
- 体验实验迭代、参数调整、模型比较和结果分析；
- 理解从研究结果到策略评价之间的关系；
- 记录研究过程中出现的重复劳动、人工操作、数据管理、实验复现等问题；
- 以这些真实体验反向推导 QuantOps 平台应该解决的问题。

最终不是形成一个优秀的量化策略，而是形成一份：

- Quant Research Workflow → MLOps Requirements  的映射。

## Phase 0 的边界

本阶段不以构建高收益策略为目标，不追求复杂 Alpha 因子，不追求复杂模型，不进入高频交易、复杂组合优化或交易执行系统研究。

模型和策略只作为 MLOps 平台未来服务的业务对象，而不是本项目最终研究目标。

## 项目称为：

Quant ML Research Experience

或者中文：量化机器学习研究体验项目
-- 量化 MLOps 系统的监控与反馈层数据库设计
-- 预测记录
-- 作用：每次模型对外提供预测时，落一条记录。这是整个监控闭环的起点。
CREATE TABLE IF NOT EXISTS predictions (
    id BIGSERIAL PRIMARY KEY,
    request_ts TIMESTAMPTZ DEFAULT NOW(),
    ticker TEXT NOT NULL,
    target_date DATE NOT NULL,
    features JSONB NOT NULL,
    prediction REAL NOT NULL,
    model_name TEXT NOT NULL,
    model_version TEXT NOT NULL,
    client_ip TEXT,
    client_version TEXT
);

CREATE INDEX IF NOT EXISTS idx_predictions_ts ON predictions(request_ts DESC);
CREATE INDEX IF NOT EXISTS idx_predictions_ticker_date ON predictions(ticker, target_date);

-- 标签（次日回填）
CREATE TABLE IF NOT EXISTS labels (
    ticker TEXT NOT NULL,
    target_date DATE NOT NULL,
    actual_return REAL NOT NULL,
    filled_ts TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (ticker, target_date)
);

-- 漂移指标
CREATE TABLE IF NOT EXISTS drift_metrics (
    id BIGSERIAL PRIMARY KEY,
    computed_ts TIMESTAMPTZ DEFAULT NOW(),
    feature_name TEXT NOT NULL,
    drift_score REAL,
    drift_detected BOOLEAN,
    method TEXT
);

CREATE INDEX IF NOT EXISTS idx_drift_ts ON drift_metrics(computed_ts DESC);

-- 服务健康日志
CREATE TABLE IF NOT EXISTS service_logs (
    id BIGSERIAL PRIMARY KEY,
    request_ts TIMESTAMPTZ DEFAULT NOW(),
    endpoint TEXT,
    status_code INT,
    latency_ms INT,
    client_ip TEXT,
    client_version TEXT
);

CREATE INDEX IF NOT EXISTS idx_service_logs_ts ON service_logs(request_ts DESC);

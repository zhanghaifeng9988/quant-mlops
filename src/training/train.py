from pathlib import Path
import pandas as pd
import numpy as np
import lightgbm as lgb
import mlflow
import mlflow.lightgbm
from sklearn.metrics import mean_squared_error

FEATURES_DIR = Path("data/features")
EXPERIMENT_NAME = "quant-mlops-walkforward"

FEATURE_COLS = [
    "ret_1d", "ret_5d", "ret_20d",
    "vol_5d", "vol_20d",
    "vol_ratio", "price_pos", "ma_ratio",
]

# (train_end, valid_end, test_end)
# 训练窗口不断扩张（expanding window）：从 4 年逐步扩到 8 年。
# 这是 walk-forward 的经典做法——模拟"随着时间推移，可用历史数据越来越多"的真实场景。
FOLDS = [
    ("2018-12-31", "2019-12-31", "2020-12-31"), # 4年训练，1年验证，1年测试
    ("2019-12-31", "2020-12-31", "2021-12-31"), # 5年训练，1年验证，1年测试
    ("2020-12-31", "2021-12-31", "2022-12-31"), # 6年训练，1年验证，1年测试
    ("2021-12-31", "2022-12-31", "2023-12-31"), # 7年训练，1年验证，1年测试
    ("2022-12-31", "2023-12-31", "2026-09-30"),  # 8年训练，1年验证，test = 2024~2026.09
]

# 按fold划分数据集
def split_by_fold(df, train_end, valid_end, test_end):
    train = df[df["date"] <= train_end]
    valid = df[(df["date"] > train_end) & (df["date"] <= valid_end)]
    test = df[(df["date"] > valid_end) & (df["date"] <= test_end)]
    return train, valid, test

# 计算每日IC -- Information Coefficient（信息系数）
# 预测值和真实收益之间的相关性——预测得越准，IC 越高。
def daily_corr(df, pred_col, label_col, method="pearson", min_n=30):
    vals = []
    for _, g in df.groupby("date"): # 按date分组，g循环获取每一天得dataframe。下划线表示不使用该变量，默认是date
        if len(g) >= min_n: # 当天股票数至少要有 min_n=30 只，才计算相关系数。
            v = g[pred_col].corr(g[label_col], method=method)
            if not np.isnan(v):
                vals.append(v)
    return float(np.mean(vals)) if vals else float("nan")

# 评估指标
# IC 衡量预测值与真实收益的日内相关性，
# RankIC 衡量预测值与真实收益的日内相关性，但考虑了预测值的排名。RankIC 用秩相关，对异常值更鲁棒，也更贴近选股场景。
def evaluate(df, pred_col="pred"):
    rmse = float(np.sqrt(mean_squared_error(df["label"], df[pred_col])))
    ic = daily_corr(df, pred_col, "label", "pearson")
    rank_ic = daily_corr(df, pred_col, "label", "spearman")
    return {"rmse": rmse, "ic": ic, "rank_ic": rank_ic}


def main():
    mlflow.set_tracking_uri('sqlite:///mlflow.db')
    mlflow.set_experiment(EXPERIMENT_NAME)

    df = pd.read_parquet(FEATURES_DIR / "features.parquet")

    params = {
        "objective": "regression",
        "metric": "rmse",
        "learning_rate": 0.05,
        "num_leaves": 31,  # 树的叶子节点数，越多越复杂，但过拟合风险也越高。
        "n_estimators": 1000,  # 树的棵树，越多越复杂，但过拟合风险也越高。
        "min_child_samples": 50,  # 叶子节点的最小样本数，防止过拟合。
        "subsample": 0.8,  # 随机采样比例，防止过拟合。
        "colsample_bytree": 0.8,  # 每棵树随机采样的特征比例，防止过拟合。
        "random_state": 42,
        "n_jobs": 4,                 # 限制核数
        "force_col_wise": True,      # 特征少时更快
        "verbose": -1,
    }

    all_results = []
# #enumerate(FOLDS, 1)   从 1 开始编号，一共有5个元组，每次循环，把一组解包成三个日期字符串
    for i, (train_end, valid_end, test_end) in enumerate(FOLDS, 1):
        train, valid, test = split_by_fold(df, train_end, valid_end, test_end)
        print(f"\n=== Fold {i} ===")
        print(f"train: {len(train):>6} rows  {train['date'].min().date()} ~ {train['date'].max().date()}")
        print(f"valid: {len(valid):>6} rows  {valid['date'].min().date()} ~ {valid['date'].max().date()}")
        print(f"test:  {len(test):>6} rows  {test['date'].min().date()} ~ {test['date'].max().date()}")

        with mlflow.start_run(run_name=f"fold-{i}") as run:
            mlflow.set_tag("fold", i) # 每个 Fold 是一个独立的 MLflow run，名字 fold-1 ~ fold-5。
            mlflow.log_params(params)
            mlflow.log_param("train_end", train_end)
            mlflow.log_param("valid_end", valid_end)
            mlflow.log_param("test_end", test_end)

            lgbm_regressor_model = lgb.LGBMRegressor(**params) # *params 把字典展开成关键字参数。
            lgbm_regressor_model.fit(
                train[FEATURE_COLS], train["label"],
                eval_set=[(valid[FEATURE_COLS], valid["label"])],
                eval_metric="rmse",
                callbacks=[lgb.early_stopping(50), lgb.log_evaluation(50)], # 验证 RMSE 连续 50 轮不改善就停止训练  50轮显示一次日志（0 表示关闭训练日志，不打印）
            )

            #  记录 feature importance (gain) 
            importance = pd.DataFrame({
                "feature": FEATURE_COLS,
                "gain": lgbm_regressor_model.booster_.feature_importance(importance_type="gain"),
            }).sort_values("gain", ascending=False).reset_index(drop=True)

            print("  feature importance (gain):")
            print(importance.to_string(index=False).replace("\n", "\n  "))

            for _, row in importance.iterrows():
                mlflow.log_metric(f"gain_{row['feature']}", row["gain"])

            importance_path = FEATURES_DIR / f"importance_fold{i}.csv"
            importance.to_csv(importance_path, index=False)
            
            # best_iteration_ = 验证集 RMSE 最低时，模型建到第几棵树。
            fold_result = {"fold": i, "best_iter": lgbm_regressor_model.best_iteration_}
           
            # 对训练集、验证集、测试集三段做统一评估
            for name, split_df in [("train", train), ("valid", valid), ("test", test)]:
                s = split_df.copy()
                s["pred"] = lgbm_regressor_model.predict(s[FEATURE_COLS])
                m = evaluate(s)
                for k, v in m.items():
                    mlflow.log_metric(f"{name}_{k}", v)
                fold_result.update({f"{name}_{k}": v for k, v in m.items()})
                print(f"{name}: rmse={m['rmse']:.5f}  ic={m['ic']:.4f}  rank_ic={m['rank_ic']:.4f}")

            mlflow.lightgbm.log_model(lgbm_regressor_model, name="models_mlflow")
            all_results.append(fold_result)
    
    # summary 
    print("\n=== Summary ===")
    res_df = pd.DataFrame(all_results)
    print(res_df.to_string(index=False))
    print(f"\nTest IC mean: {res_df['test_ic'].mean():.4f} ± {res_df['test_ic'].std():.4f}")
    print(f"Test RankIC mean: {res_df['test_rank_ic'].mean():.4f} ± {res_df['test_rank_ic'].std():.4f}")


if __name__ == "__main__":
    main()


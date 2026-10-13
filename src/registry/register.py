import argparse #解析命令行参数。
import mlflow
from mlflow.tracking import MlflowClient # 底层客户端，用来读 run、设别名、改描述。

TRACKING_URI = "sqlite:///mlflow.db"
MODEL_NAME = "us-stock-lgbm-1d"


def main():
    parser = argparse.ArgumentParser()
    # 添加 run-id 参数
    parser.add_argument("--run-id", required=True, help="MLflow run id to register")
    args = parser.parse_args()

    mlflow.set_tracking_uri(TRACKING_URI)
    client = MlflowClient()

    run = client.get_run(args.run_id)
    model_uri = run.data.tags.get("model_uri")
    if not model_uri:
        raise RuntimeError(f"run {args.run_id} has no tag 'model_uri'")

    fold = run.data.tags.get("fold")
    batch_id = run.data.tags.get("batch_id")
    test_ic = run.data.metrics.get("test_ic")
    test_rank_ic = run.data.metrics.get("test_rank_ic")

    print(f"run_id       : {args.run_id}")
    print(f"batch_id     : {batch_id}")
    print(f"fold         : {fold}")
    print(f"test_ic      : {test_ic:.4f}")
    print(f"test_rank_ic : {test_rank_ic:.4f}")
    print(f"model_uri    : {model_uri}")

    result = mlflow.register_model(model_uri=model_uri, name=MODEL_NAME)
    print(f"registered: {MODEL_NAME} version {result.version}")

    # 设置alias
    ALIAS = "candidate"

    client.set_registered_model_alias(
        name=MODEL_NAME,
        alias=ALIAS,
        version=result.version,
    )
    print(f"alias {ALIAS} set")

    client.update_model_version(
        name=MODEL_NAME,
        version=result.version,
        description=(
            f"batch_id={batch_id}, fold={fold}, "
            f"test_ic={test_ic:.4f}, test_rank_ic={test_rank_ic:.4f}"
        ),
    )


if __name__ == "__main__":
    main()
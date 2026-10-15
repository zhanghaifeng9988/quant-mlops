FROM python:3.11.16-slim-bookworm

# 设置工作目录,与开发环境的目录一致，容器内和宿主机对齐，方便查找mlflow中的数据
# 因为：db 里写死了 /home/mlops/quant-mlops-project/mlruns/1
WORKDIR /home/mlops/quant-mlops-project

RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 \
 && rm -rf /var/lib/apt/lists/* \
 && pip install uv -i https://pypi.tuna.tsinghua.edu.cn/simple

# 从官方镜像复制 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project  

COPY src/ ./src/
COPY data/features/features.parquet ./data/features/features.parquet
COPY mlflow.db ./mlflow.db
COPY mlruns/ ./mlruns/

ENV PATH="/home/mlops/quant-mlops-project/.venv/bin:$PATH"
ENV PYTHONPATH="/home/mlops/quant-mlops-project"

EXPOSE 8000

CMD ["uvicorn", "src.serving.app:app", "--host", "0.0.0.0", "--port", "8000"]


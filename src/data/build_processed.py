# 数据清洗/合并脚本——把 10 只股票的原始 parquet 合并成一个统一的 prices.parquet，
# 并做基础校验

from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA",
           "META", "TSLA", "JPM", "V", "UNH"]

# 加载单个股票数据,处理时间字段
def load_one(ticker: str) -> pd.DataFrame:
    df = pd.read_parquet(RAW_DIR / f"{ticker}.parquet") #拼路径
    # dt.tz_localize(None)	去掉时区信息    .dt.normalize()	把时间部分归零，只留日期
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None).dt.normalize()
    return df


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    frames = [load_one(t) for t in TICKERS]
    df = pd.concat(frames, ignore_index=True)

    # 统一 schema   只保留这 7 列，且按列表给定的顺序排列。
    df = df[["date", "ticker", "open", "high", "low", "close", "volume"]]
    df = df.sort_values(["date", "ticker"]).reset_index(drop=True)

    # 数据质量基础校验
    # 1. 日期和股票代码唯一，不能重复
    assert not df.duplicated(subset=["date", "ticker"]).any(), "duplicate (date, ticker)"
    # 2. OHLC 无缺失
    assert df[["open", "high", "low", "close"]].notna().all().all(), "NaN in OHLC"

    out = PROCESSED_DIR / "prices.parquet"
    df.to_parquet(out, index=False)

    print(f"saved {len(df)} rows -> {out}")
    print(f"date range: {df['date'].min().date()} ~ {df['date'].max().date()}")
    print(f"tickers: {df['ticker'].nunique()}")


if __name__ == "__main__":
    main()
# 数据清洗/合并脚本——把 100 只股票的原始 parquet 合并成一个统一的 prices.parquet，
# 并做基础校验

from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

""" tickers = [
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "BRK-B", "LLY", "AVGO", "TSLA",
    "JPM", "V", "UNH", "XOM", "MA", "JNJ", "PG", "COST", "HD", "MRK",
    "ABBV", "CVX", "WMT", "AMD", "PEP", "KO", "ADBE", "CRM", "BAC", "NFLX",
    "TMO", "LIN", "MCD", "ACN", "CSCO", "ABT", "GE", "WFC", "QCOM", "INTU",
    "TXN", "DHR", "AMGN", "CAT", "PM", "VZ", "IBM", "NOW", "UBER", "PFE",
    "RTX", "SPGI", "AXP", "GS", "ISRG", "HON", "T", "NEE", "BKNG", "LOW",
    "UNP", "COP", "ELV", "BLK", "SYK", "TJX", "VRTX", "MDT", "C", "REGN",
    "PLD", "CB", "MRSH", "ADP", "BSX", "GILD", "AMAT", "CI", "DE", "BMY",
    "ADI", "MDLZ", "SBUX", "BA", "LMT", "SCHW", "MO", "SO", "DUK", "INTC",
    "ZTS", "CVS", "PGR", "FISV", "MU", "PYPL", "EQIX", "KLAC", "ICE", "CME",
] """

# 加载单个股票数据,处理时间字段
def load_one(ticker: str) -> pd.DataFrame:
    df = pd.read_parquet(RAW_DIR / f"{ticker}.parquet") #拼路径
    # dt.tz_localize(None)	去掉时区信息    .dt.normalize()	把时间部分归零，只留日期
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None).dt.normalize()
    return df


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    tickers = sorted(p.stem for p in RAW_DIR.glob("*.parquet"))
    print(f"found {len(tickers)} tickers")
    if not tickers:
        raise RuntimeError(f"no parquet found in {RAW_DIR}")

    frames = [load_one(t) for t in tickers]
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
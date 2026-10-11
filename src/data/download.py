from pathlib import Path
from time import sleep
import yfinance as yf
import pandas as pd

import  os
proxy = 'http://172.21.160.1:7892' # 代理设置
os.environ['HTTP_PROXY'] = proxy 
os.environ['HTTPS_PROXY'] = proxy 

# Apple（苹果） Microsoft（微软） Google（谷歌） Amazon（亚马逊） NVIDIA（英伟达） 
# Meta（Facebook） Tesla（特斯拉） JPM（摩根大通） V（visa卡） UNH（UnitedHealth Group）
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA",
           "META", "TSLA", "JPM", "V", "UNH"]

START = "2015-01-01"
END = "2026-09-30"
OUT_DIR = Path("data/raw")


def download_one(ticker: str) -> pd.DataFrame:
    df = yf.download(ticker, start=START, end=END,
                     auto_adjust=True, progress=False)
    if df.empty:
        raise ValueError(f"{ticker} returned empty data")

    df = df.reset_index()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.columns = [str(c).strip().lower() for c in df.columns]
    
    # 检测压平列名后有没有重复列，有就报错
    dup = df.columns[df.columns.duplicated()].tolist()
    if dup:
        raise ValueError(f"{ticker} duplicate columns after flatten: {dup}")

    df["ticker"] = ticker
    return df


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True) # 如果目录不存在就创建，且允许多层父目录，已存在也不报错。
    for t in TICKERS:
        df = download_one(t)
        sleep(5) 
        out = OUT_DIR / f"{t}.parquet"
        df.to_parquet(out, index=False)
        print(f"{t}: {len(df)} rows -> {out}")


if __name__ == "__main__":
    main()
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import yfinance as yf
import pandas as pd
from src.data.tickers import SP100
import  os
import time

proxy = 'http://172.21.160.1:7892' # 代理设置
os.environ['HTTP_PROXY'] = proxy 
os.environ['HTTPS_PROXY'] = proxy 

# Apple（苹果） Microsoft（微软） Google（谷歌） Amazon（亚马逊） NVIDIA（英伟达） 
# Meta（Facebook） Tesla（特斯拉） JPM（摩根大通） V（visa卡） UNH（UnitedHealth Group）
# TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA",
#           "META", "TSLA", "JPM", "V", "UNH"]

START = "2015-01-01"
END = "2026-09-30"
OUT_DIR = Path("data/raw")


def download_one(ticker: str) -> pd.DataFrame:
    try:
        df = yf.download(ticker, start=START, end=END,
                         auto_adjust=True, progress=False)
    except Exception as e:
        print(f"  [{ticker}] download error: {e}")
        return None

    if df.empty:
        print(f"  [{ticker}] empty data")
        return None

    df = df.reset_index()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.columns = [str(c).strip().lower() for c in df.columns] # 上一行获取列名后，把列名统一改为小写

    # 检测压平列名后有没有重复列，有就报哪些列重复了
    dup = df.columns[df.columns.duplicated()].tolist()
    if dup:
        print(f"  [{ticker}] duplicate cols: {dup}")
        return None

    df["ticker"] = ticker
    return df


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    failed = []
    skipped = 0
    ok = 0

    for i, t in enumerate(SP100, 1):
        out = OUT_DIR / f"{t}.parquet"  # 输出文件路径
        if out.exists():
            skipped += 1
            continue

        df = download_one(t)
        if df is None:
            failed.append(t)
        else:
            df.to_parquet(out, index=False)
            ok += 1
            print(f"[{i:>3}/{len(SP100)}] {t}: {len(df)} rows")

        time.sleep(2)  # 限速，避免被 yfinance 封

    print(f"\nok={ok}  skipped={skipped}  failed={len(failed)}")
    if failed:
        (OUT_DIR / "_failed.txt").write_text("\n".join(failed))
        print(f"failed tickers saved to {OUT_DIR / '_failed.txt'}: {failed}")


if __name__ == "__main__":
    main()
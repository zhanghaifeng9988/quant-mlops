from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")

# 把 10 个 raw parquet 合成一张干净的、可校验的、带元数据的表。
# #这一步决定后面特征能不能做对。


def validate_one(ticker: str) -> dict:
    df = pd.read_parquet(RAW_DIR / f"{ticker}.parquet")

    issues = []

    # 1. 列完整
    required = {"date", "open", "high", "low", "close", "volume", "ticker"}
    missing = required - set(df.columns)
    if missing:
        issues.append(f"missing columns: {missing}")

    # 2. 日期唯一且有序
    if df["date"].duplicated().any(): #检查 date 列有没有重复值,有重复就返回 True
        issues.append(f"duplicate dates: {df['date'].duplicated().sum()}")
    if not df["date"].is_monotonic_increasing: # 检查 date 列是否按升序排列
        issues.append("dates not sorted")

    # 3. OHLC 无缺失
    for col in ["open", "high", "low", "close"]:
        n = df[col].isna().sum()
        if n:
            issues.append(f"{col} has {n} NaN")

    # 4. volume >= 0 成交量非负校验
    if (df["volume"] < 0).any(): # 检查 volume 列有没有负值,有负值就返回 True
        issues.append("negative volume")

    # 5. 最高价不能低于最低价
    if (df["high"] < df["low"]).any(): # 检查 high 列有没有小于 low 列的值,有就返回 True
        issues.append("high < low")

    return {
        "ticker": ticker,
        "rows": len(df),
        "start": df["date"].min(),
        "end": df["date"].max(),
        "issues": issues,
    }


def main():
    tickers = sorted(p.stem for p in RAW_DIR.glob("*.parquet"))
    for t in tickers:
        r = validate_one(t)
        status = "OK" if not r["issues"] else "FAIL"
        print(f"[{status}] {r['ticker']}: {r['rows']} rows, "
              f"{r['start'].date()} ~ {r['end'].date()}")
        for issue in r["issues"]:
            print(f"       - {issue}")


if __name__ == "__main__":
    main()
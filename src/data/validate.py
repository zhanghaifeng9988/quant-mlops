from pathlib import Path
import pandas as pd
# __file__ 是脚本自己的绝对路径,parents[2] 从脚本位置往上数两级
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

# 验证 raw 数据是否符合要求

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
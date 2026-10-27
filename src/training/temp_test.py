import time
from fastapi import FastAPI

app = FastAPI()

@app.get("/slow")
def slow(n: int = 0):
    time.sleep(1)   # 阻塞式 I/O：每个请求就是1个线程，1个卡 1 秒，默认最多40个线程并发
    return {"n": n, "ok": True}


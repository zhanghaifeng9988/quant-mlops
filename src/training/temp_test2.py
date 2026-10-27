# server_async.py
import asyncio
from fastapi import FastAPI

app = FastAPI()

@app.get("/slow")
async def slow(n: int = 0):
    await asyncio.sleep(1)   # 非阻塞等待：让出线程，1 秒后回来
    # 所以 1 个线程能"同时"等 多个请求——不是线程真的同时在等，是 多个协程都挂起了，
    # # 线程在它们之间流转，谁到点醒谁。
    return {"n": n, "ok": True}
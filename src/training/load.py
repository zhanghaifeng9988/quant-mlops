
# load.py  并发测试
import asyncio, aiohttp, time

async def one(session, i):
  # async with：进入后，请求真正发出；退出时自动释放响应连接。
    async with session.get(f"http://127.0.0.1:8000/slow?n={i}") as r:
        return await r.json()

async def main():
    t0 = time.time()
    async with aiohttp.ClientSession() as s: #所有 1000 个请求共用这一个 session
        await asyncio.gather(*[one(s, i) for i in range(1000)])
    print(f"1000 请求总耗时: {time.time()-t0:.2f}s")

# asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())

# 如果不用异步方式，那么请求得一条一条发
# import requests, time
# 
# def one(i):
#     r = requests.get(f"http://127.0.0.1:8000/slow?n={i}")
#     return r.json()
# 
# def main():
#     t0 = time.time()
#     for i in range(1000):
#         one(i)          # 一个一个发，发完一个等一个
#     print(f"总耗时: {time.time()-t0:.2f}s")
import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Mex World"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    responsetime = process_time
    return response


@app.get("/response")
async def responseTime():
    return add_process_time_header


@app.get("/health")
async def healthcheck():
    msg = "Endpoint is ready and live."
    return {"message": msg}

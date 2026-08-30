import time
from datetime import datetime
from edgeModel.mexapi import Edge, Video
from fastapi import FastAPI, Request
from fastapi.responses import  StreamingResponse, HTMLResponse


app = FastAPI()
edge = Edge()
video = Video()
now = datetime.now()

@app.get("/")
async def root():
    return {"message": "Hello Mex World", "ver": "7.0", "timestamp": now.strftime("%d/%m/%Y %H:%M:%S")}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/response")
async def responseTime():
    return add_process_time_header


@app.get("/registerclient")
async def edgeResponse():
    return {"message": edge.registerClient(), "timestamp": now.strftime("%d/%m/%Y %H:%M:%S")}


@app.get("/verifylocation")
async def locationResponse():
    return {"message": edge.verifyLocation(), "timestamp": now.strftime("%d/%m/%Y %H:%M:%S") }


@app.get("/getfqdn")
async def getfqdn():
    return {"fqdn": edge.getFQDN(), "timestamp": now.strftime("%d/%m/%Y %H:%M:%S")}

@app.get("/video")
async def getVideo():
    return StreamingResponse(video.getStream(), media_type = "multipart/x-mixed-replace; boundary=frame")

@app.get("/helloworld")
async def read_items():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/health")
async def healthcheck():
    msg = "Endpoint is ready and live."
    return {"message": msg , "timestamp": now.strftime("%d/%m/%Y %H:%M:%S")}

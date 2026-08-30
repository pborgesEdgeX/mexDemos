# mexDemos

A small [FastAPI](https://fastapi.tiangolo.com/) demo that showcases MobiledgeX
(Edge) matching-engine calls and streams an annotated demo video over HTTP.

The app lives in [`fastapi/`](fastapi/).

## What it does

The service exposes a handful of endpoints:

| Endpoint          | Description                                                        |
| ----------------- | ------------------------------------------------------------------ |
| `GET /`           | Basic hello/version/timestamp payload.                             |
| `GET /health`     | Health check.                                                      |
| `GET /registerclient` | Calls the Edge matching engine `findcloudlet` response.        |
| `GET /verifylocation` | Calls the Edge matching engine `verifylocation` response.     |
| `GET /getfqdn`    | Returns the cloudlet FQDN from the matching engine.               |
| `GET /video`      | Streams `videos/demovideo.mp4` as an MJPEG stream with a live timestamp overlay (OpenCV). |
| `GET /helloworld` | Returns a small static HTML page.                                 |

The Edge integration logic lives in
[`fastapi/edgeModel/mexapi.py`](fastapi/edgeModel/mexapi.py).

## Layout

```
fastapi/
├── main.py            # FastAPI app and routes
├── edgeModel/
│   └── mexapi.py      # MobiledgeX matching-engine client + video streamer
├── videos/
│   └── demovideo.mp4  # Demo clip streamed by GET /video
├── Dockerfile         # Container image (tiangolo/uvicorn-gunicorn-fastapi)
├── requirements.txt   # Python dependencies
└── edge_deploy.sh     # Helper to build/push the image to the MobiledgeX registry
```

## Run locally

```bash
cd fastapi
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export VIDEO_PATH=videos/demovideo.mp4
uvicorn main:app --reload
```

Then open http://127.0.0.1:8000/ (or `/docs` for the interactive API).

## Run with Docker

```bash
cd fastapi
docker build -t mexdemo .
docker run -p 80:80 mexdemo
```

The image sets `VIDEO_PATH=/app/videos/demovideo.mp4` so `GET /video` works out
of the box.

## Deploy

`edge_deploy.sh` builds and pushes the image to the MobiledgeX Docker registry:

```bash
cd fastapi
./edge_deploy.sh <username> <organization> <application> <version>
```

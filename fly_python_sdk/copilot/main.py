import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fly_python_sdk.fly import Fly

app = FastAPI()

templates = Jinja2Templates(
    directory=f"{os.path.dirname(os.path.realpath(__file__))}/templates"
)


@app.get("/")
async def root(request: Request):
    fly = Fly()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )

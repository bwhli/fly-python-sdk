import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fly_python_sdk.fly import Fly

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(
    directory=f"{os.path.dirname(os.path.realpath(__file__))}/templates"
)


@app.get("/app/{app_name}/")
async def root(
    request: Request,
    app_name: str,
    sort_by: str = "name",
):
    fly = Fly(os.environ["FLY_API_TOKEN"])
    machines = await fly.list_machines("nozomi-world-app-production")

    # Sort Machines by sort_by.
    machines.sort(key=lambda m: getattr(m, sort_by))

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": app_name,
            "machines": machines,
        },
    )

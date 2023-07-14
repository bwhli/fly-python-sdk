import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from rich import inspect

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
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": app_name,
            "sort_by": sort_by,
        },
    )


@app.get("/htmx/{app_name}/machines/")
async def htmx_get_machines_in_app(
    request: Request,
    app_name: str,
    sort_by: str = "name",
):
    inspect(request)

    fly = Fly(os.environ["FLY_API_TOKEN"])

    machines = await fly.list_machines(app_name)
    machines.sort(key=lambda m: getattr(m, sort_by))

    return templates.TemplateResponse(
        "htmx/machines_grid.html",
        {"request": request, "app_name": app_name, "machines": machines},
    )

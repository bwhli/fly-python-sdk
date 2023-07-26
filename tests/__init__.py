import asyncio
import hashlib
import os
from time import time

from dotenv import load_dotenv
from rich import print

from fly_python_sdk.fly import Fly

load_dotenv()

FLY_API_TOKEN = os.environ["FLY_API_TOKEN"]

# Generate a random app name to use for testing.
APP_NAME = f"random-app-{hashlib.md5(str(time()).encode()).hexdigest().lower()}"

fly = Fly(FLY_API_TOKEN)


# Create an app.
async def test_create_app():
    """
    Create an app.
    """
    app = await fly.create_app(
        app_name=APP_NAME,
        network="default",
        org_slug="personal",
    )
    print(app)


async def test_delete_app(
    app_name: str,
):
    """
    Delete an app.
    """
    app = await fly.delete_app(APP_NAME)
    print(app)


async def test_get_apps(
    org_slug: str,
    sort_by: str,
):
    """
    Get all apps in an org.
    """
    apps = await fly.get_apps(
        org_slug,
        sort_by,
    )
    print(apps)


async def test_get_app(
    app_name: str,
):
    app = await fly.get_app(app_name)
    print(app)


def test_all():
    asyncio.run(test_create_app())
    asyncio.run(test_get_apps(org_slug="personal", sort_by="name"))
    asyncio.run(test_get_app(APP_NAME))
    asyncio.run(test_delete_app(APP_NAME))

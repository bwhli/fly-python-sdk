import asyncio
import hashlib
import logging
import os
from time import time

from dotenv import load_dotenv
from rich import print

from fly_python_sdk.fly import Fly
from fly_python_sdk.models.machine import FlyMachine

logging.getLogger().setLevel(logging.DEBUG)

load_dotenv()

FLY_API_TOKEN = os.environ["FLY_API_TOKEN"]
FLY_TEST_APP_NAME = hashlib.md5(str(time()).encode()).hexdigest()
FLY_TEST_ORG_NAME = os.environ["FLY_TEST_ORG_NAME"]


def test_get_apps():
    apps = asyncio.run(Fly(FLY_API_TOKEN).Org(FLY_TEST_ORG_NAME).list_apps())
    print(apps)


def test_create_app():
    app = asyncio.run(Fly(FLY_API_TOKEN).Org(FLY_TEST_ORG_NAME).create_app(FLY_TEST_APP_NAME))  # fmt: skip
    assert app is None


def test_delete_app():
    asyncio.run(Fly(FLY_API_TOKEN).Org(FLY_TEST_ORG_NAME).App(FLY_TEST_APP_NAME).delete())  # fmt: skip


test_get_apps()

test_create_app()
test_delete_app()

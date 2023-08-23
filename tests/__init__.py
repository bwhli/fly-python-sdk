import asyncio
import hashlib
import logging
import os
from time import time

from dotenv import load_dotenv

from fly_python_sdk.fly import Fly
from fly_python_sdk.models import FlyApps, FlyMachine

logging.getLogger().setLevel(logging.DEBUG)

load_dotenv()

FLY_API_TOKEN = os.environ["FLY_API_TOKEN"]
FLY_TEST_APP_NAME = os.environ["FLY_TEST_APP_NAME"]
FLY_TEST_ORG_NAME = os.environ["FLY_TEST_ORG_NAME"]


def test_get_apps():
    apps = asyncio.run(Fly(FLY_API_TOKEN).Org(FLY_TEST_ORG_NAME).list_apps())
    logging.debug(apps)
    assert isinstance(apps, FlyApps)


def test_create_app():
    app = asyncio.run(
        Fly(FLY_API_TOKEN)
        .Org(FLY_TEST_ORG_NAME)
        .create_app(hashlib.md5(str(time()).encode()).hexdigest())
    )
    assert app is None

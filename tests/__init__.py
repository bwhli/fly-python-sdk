import asyncio
import hashlib
import os
from time import time

import rich
from dotenv import load_dotenv

from fly_python_sdk.fly import Fly

load_dotenv()

FLY_API_TOKEN = os.getenv("FLY_API_TOKEN")
FLY_TEST_APP_NAME = os.getenv("FLY_TEST_APP_NAME")

# Need to provide a valid test app name to run tests.
assert FLY_TEST_APP_NAME is not None


fly = Fly(FLY_API_TOKEN)
rich.inspect(fly)

org = fly.Org("personal")
rich.inspect(org)

app = org.App(FLY_TEST_APP_NAME)
rich.inspect(app)


def generate_random_app_name():
    return f"random-app-{hashlib.md5(str(time()).encode()).hexdigest().lower()}"

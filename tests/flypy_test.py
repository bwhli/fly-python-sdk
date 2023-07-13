import asyncio
import hashlib
import logging
import os
from datetime import datetime
from time import sleep

import pytest
from dotenv import load_dotenv

from fly_python_sdk.fly import Fly
from fly_python_sdk.models.machines import FlyMachineConfig

load_dotenv()

FLY_API_TOKEN = os.environ["FLY_API_TOKEN"]

TEST_APP_NAME = hashlib.md5(str(datetime.utcnow()).encode("utf-8")).hexdigest()

fly = Fly(FLY_API_TOKEN)


async def test_fly_create_machine():
    config = FlyMachineConfig(image="flyio/fastify-functions")
    result = await fly.create_machine("fly-python-sdk", config, region="nrt")
    assert result is not None


async def test_fly_destroy_machines():
    result = await fly.destroy_machines("fly-python-sdk", destroy_all=True)
    assert result is None


async def test_fly_wait_machine():
    result = await fly.wait_machine(
        "fly-python-sdk",
        "e2865111fe60d8",
        "stopped",
    )


asyncio.run(test_fly_create_machine())
asyncio.run(test_fly_create_machine())
asyncio.run(test_fly_create_machine())
asyncio.run(test_fly_create_machine())
sleep(5)
asyncio.run(test_fly_destroy_machines())

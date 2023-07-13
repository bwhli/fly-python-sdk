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


async def test_fly_create_machines():
    config = FlyMachineConfig(image="flyio/fastify-functions")
    tasks = [
        fly.create_machine("fly-python-sdk", config, region=region)
        for region in [
            "nrt",
            "ams",
            "dfw",
            "syd",
        ]
    ]
    result = await asyncio.gather(*tasks)
    print(result)


async def test_fly_destroy_machines():
    result = await fly.destroy_machines("fly-python-sdk", destroy_all=True)
    assert result is None


async def test_fly_wait_machine():
    result = await fly.wait_machine(
        "fly-python-sdk",
        "e2865111fe60d8",
        "stopped",
    )


print("Creating machines...")
asyncio.run(test_fly_create_machines())
print("Destroying machines...")
asyncio.run(test_fly_destroy_machines())

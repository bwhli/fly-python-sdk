import hashlib
import logging
import os
from datetime import datetime

import pytest
from dotenv import load_dotenv

from flypy.fly import Fly
from flypy.models.machines import FlyMachineConfig

load_dotenv()

FLY_API_TOKEN = os.environ["FLY_API_TOKEN"]
FLY_APP_NAME = os.environ["FLY_APP_NAME"]
FLY_ORG_SLUG = os.environ["FLY_ORG_SLUG"]

TEST_APP_NAME = hashlib.md5(str(datetime.utcnow()).encode("utf-8")).hexdigest()

fly = Fly(FLY_API_TOKEN)


# def test_fly_create_machine():
#    config = FlyMachineConfig(image="flyio/fastify-functions")
#    result = fly.create_machine("flypy", config, region="nrt")
#    assert result is not None


def test_fly_delete_machines():
    result = fly.delete_machines("flypy", delete_all=True)
    assert result is None

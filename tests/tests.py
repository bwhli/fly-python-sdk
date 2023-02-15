import hashlib
import os
from datetime import datetime

from dotenv import load_dotenv

from flypy import Fly
from flypy.models.apps import FlyAppDetailsResponse

load_dotenv()

FLY_API_TOKEN = os.environ["FLY_API_TOKEN"]
FLY_APP_NAME = os.environ["FLY_APP_NAME"]
FLY_ORG_SLUG = os.environ["FLY_ORG_SLUG"]

TEST_APP_NAME = hashlib.md5(str(datetime.utcnow()).encode("utf-8")).hexdigest()

fly = Fly(api_token=FLY_API_TOKEN)


def test_fly_create_app():
    result = fly.create_app(TEST_APP_NAME, FLY_ORG_SLUG)
    assert result is None


def test_fly_get_app():
    result = fly.get_app(FLY_APP_NAME)
    assert type(result) == FlyAppDetailsResponse


if __name__ == "__main__":
    # test_fly_get_app()
    test_fly_create_app()

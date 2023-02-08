import os

from dotenv import load_dotenv

from flypy import Fly
from flypy.models import FlyAppDetailsResponse

load_dotenv()

FLY_API_TOKEN = os.environ["FLY_API_TOKEN"]
FLY_APP_NAME = os.environ["FLY_APP_NAME"]

fly = Fly(api_token=FLY_API_TOKEN, app_name=FLY_APP_NAME)


def test_fly_get_app():
    result = fly.get_app()
    assert type(result) == FlyAppDetailsResponse


if __name__ == "__main__":
    test_fly_get_app()

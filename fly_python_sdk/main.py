import asyncio
import os

from dotenv import load_dotenv

from fly_python_sdk.fly import Fly

load_dotenv()

fly = Fly(os.environ["FLY_API_TOKEN"])

app = asyncio.run(fly.app.create("test-app"))
print(app)

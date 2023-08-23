import asyncio
import hashlib
import os
from time import time

import rich
from dotenv import load_dotenv

from fly_python_sdk.fly import Fly

load_dotenv()

FLY_API_TOKEN = os.getenv("FLY_API_TOKEN")

app = Fly(FLY_API_TOKEN).Org("personal").App("brianli-com")
app_details = asyncio.run(app.inspect())
rich.print(app_details)

machines = asyncio.run(app.list_machines(ids_only=True))
rich.print(machines)

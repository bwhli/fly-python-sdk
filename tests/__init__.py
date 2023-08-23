import asyncio
import hashlib
import logging
import os
from time import time

import rich
from dotenv import load_dotenv

from fly_python_sdk.fly import Fly

logging.getLogger().setLevel(logging.DEBUG)

load_dotenv()

FLY_API_TOKEN = os.getenv("FLY_API_TOKEN")

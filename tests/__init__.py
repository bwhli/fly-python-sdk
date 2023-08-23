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

app = Fly(FLY_API_TOKEN).Org("personal").App("brianli-com")
app_details = asyncio.run(app.inspect())
rich.print(app_details)

machines = asyncio.run(app.list_machines(ids_only=True))
rich.print(machines)

machine = app.Machine("9185727eb20298")
machine_details = asyncio.run(machine.inspect())
machine_config = machine_details.config
rich.print(machine_config)

machine_events = asyncio.run(machine.get_events())
rich.print(machine_events)

cloned_machine = asyncio.run(machine.clone(region="cdg"))
rich.print(cloned_machine)

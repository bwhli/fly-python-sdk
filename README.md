# Fly.io Python SDK (Unofficial)

## Installation

```
pip install fly-python-sdk
```

## How to Use

In order to use `fly-python-sdk`, you'll need to obtain a valid authentication token. To do this, use [flyctl's](https://github.com/superfly/flyctl) `fly auth token` command or create a new token in your Fly.io dashboard.

```
import asyncio

from fly_python_sdk.fly import Fly

fly = Fly("FLY_API_TOKEN")

# List all apps in an organization.
asyncio.run(fly.Org("org-slug").list_apps())

# Create an app.
asyncio.run(fly.Org("org-slug").App("app-name").create())

# Fetch details about an app.
asyncio.run(fly.Org("org-slug").App("app-name").inspect())


```

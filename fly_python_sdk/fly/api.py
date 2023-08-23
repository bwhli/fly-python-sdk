import httpx

from fly_python_sdk import (
    DEFAULT_API_TIMEOUT,
    FLY_MACHINES_API_DEFAULT_API_HOSTNAME,
    FLY_MACHINES_API_VERSION,
)


class FlyApi:
    """
    A class for interacting with the Fly Machines API (docs.machines.dev).
    """

    def __init__(
        self,
        api_token,
        api_timeout=DEFAULT_API_TIMEOUT,
        api_version=FLY_MACHINES_API_VERSION,
        base_url=FLY_MACHINES_API_DEFAULT_API_HOSTNAME,
    ):
        self._api_token = api_token
        self._api_timeout = api_timeout
        self._api_version = api_version
        self._base_url = base_url

    async def _make_api_delete_request(
        self,
        url_path: str,
    ) -> httpx.Response:
        """An internal function for making DELETE requests to the Fly Machines API."""
        async with httpx.AsyncClient(
            timeout=self.api_timeout,
        ) as client:
            r = await client.delete(
                f"{self.base_url}/v{self.api_version}/{url_path}",
                headers=self._generate_headers(),
            )
        return r

    async def _make_api_get_request(
        self,
        url_path: str,
    ) -> httpx.Response:
        """An internal function for making GET requests to the Fly Machines API."""
        async with httpx.AsyncClient(
            timeout=self.api_timeout,
        ) as client:
            r = await client.get(
                f"{self.base_url}/v{self.api_version}/{url_path}",
                headers=self._generate_headers(),
            )
        return r

    async def _make_api_post_request(
        self,
        url_path: str,
        payload: dict = {},
    ) -> httpx.Response:
        """An internal function for making POST requests to the Fly Machines API."""
        async with httpx.AsyncClient(
            timeout=self.api_timeout,
        ) as client:
            r = await client.post(
                f"{self.base_url}/v{self.api_version}/{url_path}",
                headers=self._generate_headers(),
                json=payload,
            )
        return r

    def _generate_headers(
        self,
    ) -> dict:
        """Returns a dictionary containing headers for requests to the Fly Machines API."""
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        return headers

"""Sample API Client."""

from __future__ import annotations

from asyncio.timeouts import timeout
from dataclasses import dataclass
import socket
from typing import Any

import aiohttp
from ampapi import ADSModule, AMPInstance, Bridge
from ampapi.dataclass import APIParams


class AmpApiClientError(Exception):
    """Exception to indicate a general API error."""


class AmpApiClientCommunicationError(
    AmpApiClientError,
):
    """Exception to indicate a communication error."""


class AmpApiClientAuthenticationError(
    AmpApiClientError,
):
    """Exception to indicate an authentication error."""


@dataclass
class AmpBaseInstance:
    """Base instance class for AMP."""

    instance_name: str
    instance_index: int


@dataclass
class AmpExtendedInstance(AmpBaseInstance):
    """Represents an extended instance of AMP (Application Management Panel)."""

    active_users: int
    players: str
    max_active_users: int
    cpu_usage_percentage: int
    memory_usage_mb: int
    app_state: str
    address: str


class AmpApiClient:
    """Sample API Client."""

    def __init__(
        self,
        username: str,
        password: str,
        host: str,
    ) -> None:
        """Sample API Client."""
        self._username = username
        self._password = password
        self._host = host
        params = APIParams(
            url=host,
            user=username,
            password=password,
        )
        Bridge(api_params=params)  # stores params statically so available globally
        self.ads: ADSModule = ADSModule()

    async def async_get_instances(self) -> list[AmpBaseInstance]:
        """Asynchronously retrieves a list of AMP base instances.

        This method fetches the available instances from the ADS
        and returns a list of `AmpBaseInstance` objects, each containing the instance name and index.

        Returns:
            list[AmpBaseInstance]: A list of AMP base instances.

        """
        instances = (await self.ads.get_instances())[0].available_instances
        return [
            AmpBaseInstance(
                instance_name=instance.friendly_name,
                instance_index=index,
            )
            for index, instance in enumerate(instances)
        ]

    async def async_get_data(self) -> dict[int, AmpExtendedInstance]:
        """Get data from the API."""

        all_instances = (await self.ads.get_instances())[0].available_instances
        data = {}
        for key, instance in enumerate(all_instances):
            instance_data = AMPInstance(instance)
            players_raw = (await instance_data.get_user_list()).sorted
            players = (
                ", ".join(player.name for player in players_raw)
                if players_raw
                else None
            )
            active_users = (
                instance_data.metrics.active_users.get("raw_value", 0)
                if instance_data.metrics.active_users
                else 0
            )
            max_active_users = (
                instance_data.metrics.active_users.get("max_value", 0)
                if instance_data.metrics.active_users
                else 0
            )
            cpu_usage_percentage = (
                instance_data.metrics.cpu_usage.get("raw_value", 0)
                if instance_data.metrics.cpu_usage
                else 0
            )
            memory_usage_mb = (
                instance_data.metrics.memory_usage.get("raw_value", 0)
                if instance_data.metrics.memory_usage
                else 0
            )
            app_state = instance_data.app_state.name
            address = instance_data.application_endpoints[0]["endpoint"]
            data[key] = AmpExtendedInstance(
                instance_name=instance.friendly_name,
                instance_index=key,
                active_users=active_users,
                players=players,
                max_active_users=max_active_users,
                cpu_usage_percentage=cpu_usage_percentage,
                memory_usage_mb=memory_usage_mb,
                app_state=app_state,
                address=address,
            )
        return data

    async def async_set_title(self, value: str) -> Any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="patch",
            url="https://jsonplaceholder.typicode.com/posts/1",
            data={"title": value},
            headers={"Content-type": "application/json; charset=UTF-8"},
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            async with timeout(10):
                instances = await self.ads.get_instances()
                instance: AMPInstance = AMPInstance(instances[1])
                return instance.metrics.active_users.raw_value

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise AmpApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise AmpApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:
            msg = f"Something really wrong happened! - {exception}"
            raise AmpApiClientError(
                msg,
            ) from exception

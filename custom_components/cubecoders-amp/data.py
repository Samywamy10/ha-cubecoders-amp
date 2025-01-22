"""Custom types for integration_blueprint."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.loader import Integration

from .api import AmpApiClient
from .coordinator import AmpDataUpdateCoordinator

type AMPConfigEntry = ConfigEntry[AmpData]


@dataclass
class AmpData:
    """Data for the Blueprint integration."""

    client: AmpApiClient
    coordinator: AmpDataUpdateCoordinator
    integration: Integration

"""Module contains the entry setup for the CubeCoders integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry

from .data import AmpData

type AMPConfigEntry = ConfigEntry[AmpData]

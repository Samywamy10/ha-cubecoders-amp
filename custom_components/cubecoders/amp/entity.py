"""Module for CubeCoders AMP integration entities."""

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import AmpDataUpdateCoordinator


class AMPEntity(CoordinatorEntity[AmpDataUpdateCoordinator]):
    """BlueprintEntity class."""

    _attr_attribution = "Attribution"

    def __init__(self, coordinator: AmpDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    coordinator.config_entry.domain,
                    coordinator.config_entry.entry_id,
                ),
            },
        )

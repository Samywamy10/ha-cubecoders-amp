"""Sensor platform for integration_blueprint."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, UnitOfInformation
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import AmpBaseInstance
from .entity import AMPEntity
from .entry import AMPConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: AMPConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    instances = await entry.runtime_data.client.async_get_instances()
    all_entities = []
    for instance in instances:
        if instance.instance_name == "ADS":
            continue
        device = DeviceInfo(
            identifiers={("cubecoders", instance.instance_name)},
            name=instance.instance_name,
            manufacturer="CubeCoders",
        )
        sensor_entities = [
            AmpSensor(
                entry,
                instance,
                device,
                name="Active Users",
                key="active_users",
                icon="mdi:account-group",
                state_class=SensorStateClass.MEASUREMENT
            ),
            AmpSensor(
                entry,
                instance,
                device,
                name="Players",
                key="players",
                icon="mdi:account-group",
            ),
            AmpSensor(
                entry,
                instance,
                device,
                name="Max Active Users",
                key="max_active_users",
                icon="mdi:account-group",
                state_class=SensorStateClass.MEASUREMENT
            ),
            AmpSensor(
                entry,
                instance,
                device,
                name="CPU Usage %",
                key="cpu_usage_percentage",
                icon="mdi:cpu-64-bit",
                native_unit_of_measurement=PERCENTAGE,
            ),
            AmpSensor(
                entry,
                instance,
                device,
                name="Memory Usage",
                key="memory_usage_mb",
                device_class=SensorDeviceClass.DATA_SIZE,
                native_unit_of_measurement=UnitOfInformation.MEGABYTES,
            ),
            AmpSensor(
                entry,
                instance,
                device,
                name="App state",
                key="app_state",
            ),
            AmpSensor(
                entry,
                instance,
                device,
                name="Address",
                key="address",
            ),
        ]
        all_entities.extend(sensor_entities)

    async_add_entities(all_entities)


class AmpSensor(AMPEntity, SensorEntity):
    """integration_blueprint Sensor class."""

    def __init__(
        self,
        entry: AMPConfigEntry,
        instance: AmpBaseInstance,
        device: DeviceInfo,
        name: str,
        key: str,
        device_class: SensorDeviceClass | None = None,
        state_class: SensorStateClass | None = None,
        native_unit_of_measurement: str | None = None,
        icon: str | None = None,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(entry.runtime_data.coordinator)
        entity_key = f"{instance.instance_index}_{instance.instance_name}_{key}"
        self.entity_description = SensorEntityDescription(
            key=entity_key,
            name=f"{instance.instance_name} {name}",
            icon=icon,
            device_class=device_class,
            native_unit_of_measurement=native_unit_of_measurement,
            state_class=state_class,
            # suggested_unit_of_measurement=suggested_unit_of_measurement,
        )
        self.key = key
        self._attr_unique_id = entity_key
        self.index = instance.instance_index
        self.device = device

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return getattr(self.coordinator.data[self.index], self.key)

    @property
    def device_info(self) -> DeviceInfo:
        """Returns the device information."""
        return self.device

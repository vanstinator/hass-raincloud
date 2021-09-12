"""Support for Melnor RainCloud sprinkler water timer."""
import logging

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_MONITORED_CONDITIONS
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.icon import icon_for_battery_level

from . import DATA_RAINCLOUD, ICON_MAP, SENSORS, RainCloudEntity

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_MONITORED_CONDITIONS, default=list(SENSORS)): vol.All(
            cv.ensure_list, [vol.In(SENSORS)]
        )
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up a sensor for a raincloud device."""
    raincloud = hass.data[DATA_RAINCLOUD].data

    sensors = []
    for sensor_type in config.get(CONF_MONITORED_CONDITIONS):
        if sensor_type == "battery":
            for controller in raincloud.controllers:                
                for faucet in controller.faucets:
                    sensors.append(RainCloudSensor(faucet, sensor_type))

        else:
            # create a sensor for each zone managed by controller and faucet
            for controller in raincloud.controllers:
                for faucet in controller.faucets:
                    for zone in faucet.zones:
                        sensors.append(RainCloudSensor(zone, sensor_type))

    add_entities(sensors, True)
    return True


class RainCloudSensor(RainCloudEntity):
    """A sensor implementation for raincloud device."""

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update(self):
        """Get the latest data and updates the states."""
        _LOGGER.debug("Updating RainCloud sensor: %s", self._name)
        if self._sensor_type == "battery":
            self._state = self.data.battery
        else:
            self._state = getattr(self.data, self._sensor_type)

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        if self._sensor_type == "battery" and self._state is not None:
            return icon_for_battery_level(
                battery_level=int(self._state), charging=False
            )
        return ICON_MAP.get(self._sensor_type)

    @property
    def device_class(self):
        if self._sensor_type == "battery":
            return "battery"

    @property
    def state_class(self):
        if self._sensor_type == "battery":
            return "measurement"
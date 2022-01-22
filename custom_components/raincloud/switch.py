"""Support for Melnor RainCloud sprinkler water timer."""
import logging

import voluptuous as vol

from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchEntity
from homeassistant.const import ATTR_ATTRIBUTION, CONF_MONITORED_CONDITIONS
import homeassistant.helpers.config_validation as cv

from . import (
    ALLOWED_WATERING_TIME,
    ATTRIBUTION,
    CONF_WATERING_TIME,
    DATA_RAINCLOUD,
    DEFAULT_WATERING_TIME,
    SWITCHES,
    RainCloudEntity,
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_MONITORED_CONDITIONS, default=list(SWITCHES)): vol.All(
            cv.ensure_list, [vol.In(SWITCHES)]
        ),
        vol.Optional(CONF_WATERING_TIME, default=DEFAULT_WATERING_TIME): vol.All(
            vol.In(ALLOWED_WATERING_TIME)
        ),
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up a sensor for a raincloud device."""
    raincloud = hass.data[DATA_RAINCLOUD].data
    default_watering_timer = config.get(CONF_WATERING_TIME)

    sensors = []
    for sensor_type in config.get(CONF_MONITORED_CONDITIONS):
        # create a sensor for each zone managed by faucet
        for controller in raincloud.controllers:
            for faucet in controller.faucets:
                for zone in faucet.zones:
                    sensors.append(RainCloudSwitch(
                        default_watering_timer, zone, sensor_type))

    add_entities(sensors, True)


class RainCloudSwitch(RainCloudEntity, SwitchEntity):
    """A switch implementation for raincloud device."""

    def __init__(self, default_watering_timer, *args):
        """Initialize a switch for raincloud device."""
        super().__init__(*args)
        self._default_watering_timer = default_watering_timer

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Turn the device on."""
        if self._sensor_type == "manual_watering":
            self.data.manual_watering = self._default_watering_timer
        elif self._sensor_type == "auto_watering":
            self.data.auto_watering = True
        self._state = True

    def turn_off(self, **kwargs):
        """Turn the device off."""
        if self._sensor_type == "manual_watering":
            self.data.manual_watering = "off"
        elif self._sensor_type == "auto_watering":
            self.data.auto_watering = False
        self._state = False

    def update(self):
        """Update device state."""
        _LOGGER.debug("Updating RainCloud switch: %s", self._name)
        if self._sensor_type == "manual_watering":
            self._state = bool(self.data.manual_watering)
        elif self._sensor_type == "auto_watering":
            self._state = self.data.auto_watering

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            ATTR_ATTRIBUTION: ATTRIBUTION,
            "default_manual_timer": self._default_watering_timer,
            "identifier": self.data.serial,
        }

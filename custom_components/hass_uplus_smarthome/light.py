from __future__ import annotations

from pprint import pformat
import voluptuous as vol
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation, typing
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import DiscoveryInfoType

from custom_components.hass_uplus_smarthome.const import LOGGER
from custom_components.hass_uplus_smarthome.uplus_api import MoodLightAPI
from homeassistant.components.light import SUPPORT_BRIGHTNESS, PLATFORM_SCHEMA, LightEntity, ATTR_BRIGHTNESS

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): config_validation.string
})


def setup_platform(
        hass: HomeAssistant,
        config: typing.ConfigType,
        add_entities: AddEntitiesCallback,
        discovery_info: DiscoveryInfoType | None = None
) -> None:
    # Add devices
    LOGGER.info(pformat(config))

    name = config[CONF_NAME]

    add_entities([UplusMoodLight(name=name)])


class UplusMoodLight(LightEntity):

    def __init__(self, name) -> None:
        super().__init__()
        self.api = MoodLightAPI()
        # self._light_color = '#ffffff'
        self._brightness = 0
        self._state = None
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def brightness(self) -> int | None:
        return self._brightness

    @property
    def supported_features(self) -> int:
        return SUPPORT_BRIGHTNESS

    @property
    def is_on(self) -> bool | None:
        return self._state

    def get_session(self):
        return async_get_clientsession(self.hass)

    async def async_turn_on(self, **kwargs) -> None:
        if ATTR_BRIGHTNESS in kwargs:
            self._brightness = kwargs[ATTR_BRIGHTNESS]
            await self.api.set_brightness(self.get_session(), int(self._brightness / 2.55))
            return

        await self.api.light_turn_on(self.get_session())

    async def async_turn_off(self, **kwargs) -> None:
        await self.api.light_turn_off(self.get_session())

    async def async_update(self):
        result = await self.api.update(self.get_session())
        self._state = bool(int(result['device_status']))
        self._brightness = int(result['brightness']) * 2.55

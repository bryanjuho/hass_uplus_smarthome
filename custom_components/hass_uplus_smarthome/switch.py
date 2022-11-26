from pprint import pformat

from homeassistant.helpers import typing
from homeassistant.core import HomeAssistant
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import DiscoveryInfoType
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.hass_uplus_smarthome.const import LOGGER
from custom_components.hass_uplus_smarthome.uplus_api import PowerSwitchAPI


def setup_platform(
        hass: HomeAssistant,
        config: typing.ConfigType,
        add_entities: AddEntitiesCallback,
        discovery_info: DiscoveryInfoType | None = None
) -> None:
    # Add devices
    LOGGER.info(pformat(config))

    entities = [
        UplusPowerSwitch(idx=1),
        UplusPowerSwitch(idx=2),
        UplusPowerSwitch(idx=3),
        UplusPowerSwitch(idx=4)
    ]

    add_entities(entities)


class UplusPowerSwitch(SwitchEntity):
    def __init__(self, idx):
        super().__init__()
        self.api = PowerSwitchAPI()
        self._idx = idx
        self._state = None

    @property
    def is_on(self) -> bool | None:
        return self._state

    @property
    def name(self) -> str:
        return f"멀티탭 {self._idx}구"

    def get_session(self):
        return async_get_clientsession(self.hass)

    async def async_turn_on(self, **kwargs) -> None:
        await self.api.async_turn_on(self.get_session(), self._idx)

    async def async_turn_off(self, **kwargs) -> None:
        await self.api.async_turn_off(self.get_session(), self._idx)

    async def async_update(self):
        self._state = await self.api.update(self.get_session(), self._idx)

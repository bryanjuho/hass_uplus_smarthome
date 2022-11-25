from __future__ import annotations

import json
import logging
from typing import Any

import requests
from pprint import pformat, pprint
import voluptuous as vol
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import config_validation, typing
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import DiscoveryInfoType

from custom_components.hass_uplus_smarthome.const import PowerStatus
from custom_components.hass_uplus_smarthome.utils import datetime_string, random_token

_LOGGER = logging.getLogger('uplus')
from custom_components.hass_uplus_smarthome.uplus_api import MoodLightAPI
from homeassistant.components.light import SUPPORT_BRIGHTNESS, PLATFORM_SCHEMA, LightEntity

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
    _LOGGER.info(pformat(config))

    name = config[CONF_NAME]

    add_entities([UplusMoodLight(name=name)])


class UplusMoodLight(LightEntity):
    def turn_on(self, **kwargs: Any) -> None:
        pass

    def turn_off(self, **kwargs: Any) -> None:
        pass

    def __init__(self, name) -> None:
        self.api = MoodLightAPI()
        self._power = PowerStatus.UNKNOWN
        self._light_color = '#ffffff'
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

    async def async_turn_on(self, **kwargs) -> None:
        await self.api.light_turn_on()

    async def async_turn_off(self, **kwargs) -> None:
        await self.api.light_turn_off()

    async def async_update(self):
        session = async_get_clientsession(self.hass)
        url = 'https://hmiotsas.uplus.co.kr:7002/smartlight/ws/smartlight/common/getDeviceStatusThings'
        headers = {
            'Host': 'hmiotsas.uplus.co.kr:7002',
            'X-HIT-Version': 'v3',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'X-HIT-Log-Key': f'{datetime_string()}.{random_token(upper=True, k=4)}.SLGT',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://hmiotsas.uplus.co.kr:7002',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Referer': 'https://hmiotsas.uplus.co.kr:7002/smartlight/smartlight/main.html?mid=LC100&uuid=93BAB3FB-292B-34AC-93E1-70DDD599181C&pmid=HS001&vendor=0000584&model=LT-Z24C01',
            'X-HIT-SvcCode': '9119',
            'Content-Length': '411',
            'X-HIT-Channel': 'APP-SMARTLIGHT',
            'X-HIT-Vendor': '0000584',
            'Content-Type': 'application/json'
        }
        data = {'account': {'one_id': 'sallyhaeri@hanmail.net', 'one_id_key': '4003915545',
                            'sso_key': '72aa86051a9068a26fde078994a3bd18',
                            'session_key': 'H000101_20C6D637-9B3F-4E57-A092-3F9A4509BBC6_H585LNPS1RMXEOAOAD9M'},
                'home': {'home_code': '500123840867'},
                'device': {'uuid': '93BAB3FB-292B-34AC-93E1-70DDD599181C', 'model': 'LT-Z24C01'}, 'mid': 'LC100',
                'parameter': {'agsset': {'cmd_request': {'cmd_id': 2, 'parameters': [{'filter': 'ALL'}]}}}}

        async with session.post(
                url=url,
                headers=headers,
                json=data,
                timeout=10
        ) as response:
            result = await response.json()
            response.raise_for_status()
            statuses = result['parameter']['cmd_report']['parameters']

            params = ['device_status', 'brightness', 'color']
            status_to_dict = {k: v for status in statuses for k, v in status.items() if k in params}
            self.api.light.is_on = bool(int(status_to_dict['device_status']))
            self.api.light.brightness = int(status_to_dict['brightness']) * 2.55
            self._state = self.api.light.is_on
            self._brightness = self.api.light.brightness

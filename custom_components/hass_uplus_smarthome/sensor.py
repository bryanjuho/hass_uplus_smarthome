from homeassistant.helpers.entity import Entity

from custom_components.hass_uplus_smarthome import DOMAIN
from custom_components.hass_uplus_smarthome.const import PowerStatus
from custom_components.hass_uplus_smarthome.uplus_api import PowerExtensionAPI, MoodLightAPI


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up sensor for Naver Weather sensors."""

    api = hass.data[DOMAIN]["api"][config_entry.entry_id]

    def async_add_entity():
        """Add sensor from sensor."""
        entities = [
            UplusPowerExtension(api=PowerExtensionAPI()),
            UplusMoodLight(api=MoodLightAPI())
        ]

        async_add_entities(entities)

    async_add_entity()


class Outlet:

    def __init__(self, index):
        self.index = index
        self.state = PowerStatus.UNKNOWN
        self.label = ''


class UplusDeviceBase(Entity):

    def __init__(self, api):
        self.power = PowerStatus.UNKNOWN
        self.api = api


class UplusPowerExtension(UplusDeviceBase):
    count_outlets = 4

    def __init__(self, api):
        super().__init__(api=api)
        self.outlets = [Outlet(i) for i in range(1, self.count_outlets + 1)]

    @property
    def state(self):
        values = self.api.results
        return values


class UplusMoodLight(UplusDeviceBase):

    def __init__(self, api):
        super().__init__(api=api)
        self.light_color = '#ffffff'
        self.light_brightness = 0

    @property
    def state(self):
        values = self.api.results
        return values

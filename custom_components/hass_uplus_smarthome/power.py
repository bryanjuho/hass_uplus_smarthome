from custom_components.hass_uplus_smarthome.uplus_api import PowerExtensionAPI


async def async_setup_entry(hass, config_entry, async_add_entities):
    def async_add_entity():
        """Add sensor from sensor."""
        entities = [
            UplusPowerExtension(api=PowerExtensionAPI())
        ]

        async_add_entities(entities)

    async_add_entity()


class Outlet:

    def __init__(self, index):
        self.index = index
        self.state = PowerStatus.UNKNOWN
        self.label = ''


class UplusPowerExtension(UplusDeviceBase):
    count_outlets = 4

    def __init__(self, api):
        super().__init__(api=api)
        self.outlets = [Outlet(i) for i in range(1, self.count_outlets + 1)]

    @property
    def state(self):
        values = self.api.results
        return values

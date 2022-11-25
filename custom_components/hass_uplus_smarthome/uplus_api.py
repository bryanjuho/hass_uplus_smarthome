import logging

_LOGGER = logging.getLogger('uplus')


class PowerExtensionAPI:

    async def update(self):
        pass

    @property
    def results(self):
        return [1, 1, 0, 0]


class MoodLightAPI:
    class Light:
        def __init__(self):
            self.is_on = False
            self.brightness = 0

    def __init__(self):
        self.light = self.Light()

    async def update(self):
        pass

    async def light_turn_on(self):
        _LOGGER.info("turn_on")

    async def light_turn_off(self):
        _LOGGER.info("turn_off")

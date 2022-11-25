import requests
from . import const


class UplusAPIBase:
    base_url = const.UPLUS_API_BASE_URL

    def __init__(self):
        pass

    async def update(self):
        raise NotImplementedError


class PowerExtensionAPI(UplusAPIBase):

    async def update(self):
        pass

    @property
    def results(self):
        return [1, 1, 0, 0]


class MoodLightAPI(UplusAPIBase):

    async def update(self):
        pass

    @property
    def results(self):
        return [1, 55]

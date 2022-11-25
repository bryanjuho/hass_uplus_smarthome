"""Constants for the hass_uplus_smarthome integration."""
from enum import Enum

DOMAIN = "hass_uplus_smarthome"

PLATFORMS = ["light", "switch"]

UPLUS_API_BASE_URL = 'https://'


class PowerStatus(Enum):
    ON = 1
    OFF = 0
    UNKNOWN = -1

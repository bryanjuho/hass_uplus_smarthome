import json
from pprint import pprint

import requests

from custom_components.hass_uplus_smarthome.utils import datetime_string, random_token

if __name__ == '__main__':
    url = 'https://hmiotapi.uplus.co.kr:9443/homeiot/package/onepartner/device_status'
    idx = 1
    headers_common = {
        'Host': 'hmiotapi.uplus.co.kr:9443',
        'X-HIT-Vendor': '0000564',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://hmiotsvc.uplus.co.kr:8070',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_1 like Mac OS X)'
                      ' AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Connection': 'keep-alive',
        'Referer': 'https://hmiotsvc.uplus.co.kr:8070/',
        'X-HIT-Version': 'v2',
        'Content-Type': 'application/json'
    }
    headers = {
        **headers_common,
        'Content-Length': '375'
    }
    data = {'account': {'one_id': 'sallyhaeri@hanmail.net', 'one_id_key': '4003915545',
                        'sso_key': '72aa86051a9068a26fde078994a3bd18',
                        'session_key': 'H000101_20C6D637-9B3F-4E57-A092-3F9A4509BBC6_H585LNPS1RMXEOAOAD9M'},
            'home': {'home_code': '500123840867'}, 'device': {'uuid': 'FE90F3AF-D03F-345D-A531-434297764DB5'},
            'cmd_request': {'cmd_id': 2, 'parameters': [{'command': 'STATUS_GET', 'filter': 'ALL'}]}}

    with requests.post(url, headers=headers, json=data) as response:
        result = response.json()
        _is_on = result['cmd_report']['parameters'][idx][f'switchBinary{idx}']

    pprint(response.json())

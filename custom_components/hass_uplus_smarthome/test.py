import json
from pprint import pprint

import requests

from custom_components.hass_uplus_smarthome.utils import datetime_string, random_token

if __name__ == '__main__':
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
    response = requests.post(
        url=url,
        headers=headers,
        # data=json.dumps(data),
        timeout=2
    )
    pprint(response.json())

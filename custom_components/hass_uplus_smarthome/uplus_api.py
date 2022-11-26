from pprint import pformat

from custom_components.hass_uplus_smarthome.const import LOGGER
from custom_components.hass_uplus_smarthome.utils import datetime_string, random_token


class PowerSwitchAPI:
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

    async def update(self, session, idx):
        url = 'https://hmiotapi.uplus.co.kr:9443/homeiot/package/onepartner/device_status'

        headers = {
            **self.headers_common,
            'Content-Length': '375'
        }
        data = {'account': {'one_id': 'sallyhaeri@hanmail.net', 'one_id_key': '4003915545',
                            'sso_key': '72aa86051a9068a26fde078994a3bd18',
                            'session_key': 'H000101_20C6D637-9B3F-4E57-A092-3F9A4509BBC6_H585LNPS1RMXEOAOAD9M'},
                'home': {'home_code': '500123840867'}, 'device': {'uuid': 'FE90F3AF-D03F-345D-A531-434297764DB5'},
                'cmd_request': {'cmd_id': 2, 'parameters': [{'command': 'STATUS_GET', 'filter': 'ALL'}]}}

        async with session.post(url, headers=headers, json=data) as response:
            response.raise_for_status()
            result = await response.json()
            LOGGER.debug(pformat(result))
            _is_on = result['cmd_report']['parameters'][idx][f'switchBinary{idx}']
            return _is_on == 'FF'

    async def async_turn_on(self, session, idx):
        await self.async_toggle(session, 'on', idx)

    async def async_turn_off(self, session, idx):
        await self.async_toggle(session, 'off', idx)

    async def async_toggle(self, session, state, idx):
        url = 'https://hmiotapi.uplus.co.kr:9443/homeiot/package/onepartner/device_control'
        value = 'FF' if state == 'on' else '00'

        data = {'account': {'one_id': 'sallyhaeri@hanmail.net', 'one_id_key': '4003915545',
                            'sso_key': '72aa86051a9068a26fde078994a3bd18',
                            'session_key': 'H000101_20C6D637-9B3F-4E57-A092-3F9A4509BBC6_H585LNPS1RMXEOAOAD9M'},
                'home': {'home_code': '500123840867'}, 'device': {'uuid': 'FE90F3AF-D03F-345D-A531-434297764DB5'},
                'cmd_request': {'cmd_id': 1,
                                'parameters': [{'command': f'POWER{idx}_SET', f'switchBinary{idx}': value}]}}

        headers = {
            **self.headers_common,
            'Content-Length': '381'
        }
        async with session.post(
                url=url,
                headers=headers,
                json=data,
                timeout=10
        ) as response:
            response.raise_for_status()


class MoodLightAPI:
    headers_common = {
        'Host': 'hmiotsas.uplus.co.kr:7002',
        'X-HIT-Version': 'v3',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://hmiotsas.uplus.co.kr:7002',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_1 like Mac OS X)'
                      ' AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Referer': 'https://hmiotsas.uplus.co.kr:7002/smartlight/smartlight/main.html?mid=LC100'
                   '&uuid=93BAB3FB-292B-34AC-93E1-70DDD599181C&pmid=HS001&vendor=0000584&model=LT-Z24C01',
        'X-HIT-SvcCode': '9119',
        'X-HIT-Channel': 'APP-SMARTLIGHT',
        'X-HIT-Vendor': '0000584',
        'Content-Type': 'application/json',
    }

    async def update(self, session):
        url = 'https://hmiotsas.uplus.co.kr:7002/smartlight/ws/smartlight/common/getDeviceStatusThings'
        data = {
            'account': {
                'one_id': 'sallyhaeri@hanmail.net',
                'one_id_key': '4003915545',
                'sso_key': '72aa86051a9068a26fde078994a3bd18',
                'session_key': 'H000101_20C6D637-9B3F-4E57-A092-3F9A4509BBC6_H585LNPS1RMXEOAOAD9M'
            },
            'home': {'home_code': '500123840867'},
            'device': {'uuid': '93BAB3FB-292B-34AC-93E1-70DDD599181C', 'model': 'LT-Z24C01'}, 'mid': 'LC100',
            'parameter': {'agsset': {'cmd_request': {'cmd_id': 2, 'parameters': [{'filter': 'ALL'}]}}}
        }
        headers = {
            **self.headers_common,
            'X-HIT-Log-Key': f'{datetime_string()}.{random_token(upper=True)}.SLGT',
            'Referer': 'https://hmiotsas.uplus.co.kr:7002/smartlight/smartlight/main.html?mid=LC100'
                       '&uuid=93BAB3FB-292B-34AC-93E1-70DDD599181C&pmid=HS001&vendor=0000584&model=LT-Z24C01',
            # 'Content-Length': len(json.dumps(data, separators=(',', ':')))
            'Content-Length': '411'
        }

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
            return {k: v for status in statuses for k, v in status.items() if k in params}

    async def light_turn_on(self, session):
        LOGGER.info('turn_on')
        await self.toggle_light(session, 'on')
        LOGGER.info('turn_on success')

    async def light_turn_off(self, session):
        LOGGER.info("turn_off")
        await self.toggle_light(session, 'off')
        LOGGER.info('turn_off success')

    async def toggle_light(self, session, state):
        url = 'https://hmiotsas.uplus.co.kr:7002/smartlight/ws/smartlight/common/setControl'
        data = {'account': {'one_id': 'sallyhaeri@hanmail.net', 'one_id_key': '4003915545',
                            'sso_key': '72aa86051a9068a26fde078994a3bd18',
                            'session_key': 'H000101_20C6D637-9B3F-4E57-A092-3F9A4509BBC6_H585LNPS1RMXEOAOAD9M'},
                'home': {'home_code': '500123840867'},
                'device': {'uuid': '93BAB3FB-292B-34AC-93E1-70DDD599181C', 'model': 'LT-Z24C01'}, 'mid': 'LC100',
                'parameter': {'agsset': {
                    'cmd_request': {'cmd_id': 1, 'parameters': [{'device_status': '1' if state == 'on' else '0'}]}}}}
        headers = {
            **self.headers_common,
            'X-HIT-Log-Key': f'{datetime_string()}.{random_token(upper=True)}.SLGT',
            'Content-Length': '416'
        }
        async with session.post(
                url=url,
                headers=headers,
                json=data,
                timeout=10
        ) as response:
            response.raise_for_status()

    async def set_brightness(self, session, brightness):
        LOGGER.info('set_brightness')
        url = 'https://hmiotsas.uplus.co.kr:7002/smartlight/ws/smartlight/common/setControl'
        data = {'account': {'one_id': 'sallyhaeri@hanmail.net', 'one_id_key': '4003915545',
                            'sso_key': '72aa86051a9068a26fde078994a3bd18',
                            'session_key': 'H000101_20C6D637-9B3F-4E57-A092-3F9A4509BBC6_H585LNPS1RMXEOAOAD9M'},
                'home': {'home_code': '500123840867'},
                'device': {'uuid': '93BAB3FB-292B-34AC-93E1-70DDD599181C', 'model': 'LT-Z24C01'}, 'mid': 'LC100',
                'parameter': {'agsset': {
                    'cmd_request': {'cmd_id': 1, 'parameters': [{'brightness': str(brightness).zfill(3)}]}}}}

        headers = {
            **self.headers_common,
            'X-HIT-Log-Key': f'{datetime_string()}.{random_token(upper=True)}.SLGT',
            'Content-Length': '415'
        }
        async with session.post(
                url=url,
                headers=headers,
                json=data,
                timeout=10
        ) as response:
            response.raise_for_status()
        LOGGER.info('set_brightness success')

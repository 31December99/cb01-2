# -*- coding: utf-8 -*-
import json
import requests


class Stayonline:
    # reCaptha2 token # todo scade ?

    result = {
        'code': '03AFcWeA7J7j0nzzWQ769di2Ze2qKwnjWCcC-xFSaSAtCYsKn-DY21Rz2sA-TsEaTWM9j94zr5T1s2ebAZoeGdlVtSsvvKR3JHtX'
                'TDxypRHlbo18yy5uvc6bkerIJ1YaKLcraWv8CCyWVb4Dme7S1QLs1QRv5oMRhyVdTtiyJ7o9i9uyUCMLplc6PlE0EW4Vytzuatbq'
                'JjzoJP4aMrTwzRpUOrBqW-1u2zJU7_k3Vi0nKKODpO6YixOIDcbfPRxsDMeIpiovRaqbn_PaNY7uEC6Lx4o6qORXJpSdWj-9twAp'
                'JrvZfg2RjRLzCy1BQcqTYa-UfzaVEV8vQDNYUQwFCsR_1R8XqsZ8R2cLRLBneA5HMTuf2JyklCjTSw_T987NblAh7jurgv1vjzNo'
                'OqXUo_t0z38lpi-27wmXIjr7KHKTfybX88u_cboQLiw3d4rPLS26VtgREESM2Uc4P21R19hIWolcDK7wMroRIJD85ZYEM9LrHgN5'
                'pqTEtpMWxiaM76oBGQxIjV7aFjMWlI8T_6XCUj6P_mQwvFP9ws9Xw8gi2KLdwqzMaP7Rgt3MjhQd43ecz0hGcMh_bEbmjVfkTSlU'
                'taiktVy20nPwckJA8_YVvlIZIMCR1iQfB1xbn9Pz03P2j7F8RI-QPoY3CGk33B1xcteOXPhlaeg5GDCII8owbYeQ9V-HgeCC4Gm6'
                'aaaGz-s7ObQSfK0KbOd2mV43lUBrVWfFxLAZDVBycNovjE9OdBjswR5Zrc8KwkFyDSE7bjQIQD68jmlh2jFp6MsxeAtIOoinyelj'
                'QYvQ'}

    cookies = ''
    headers = ''
    data = ''

    @classmethod
    def get_url(cls, url: str) -> str:
        id = url.split('/')[4]

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://stayonline.pro',
            'Alt-Used': 'stayonline.pro',
            'Connection': 'keep-alive',
            'Referer': url,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }

        cookies = {
            '_ga_HE603D8QBD': 'GS1.1.1719509256.3.1.1719509426.0.0.0',
            '_ga': 'GA1.2.1202250886.1719436520',
            '_gid': 'GA1.2.362858314.1719436521',
            'a': 'XZBsauJA9vOaN3Jp5MT32Vv8g0fTVykc',
            'token_QpUJAAAAAAAAGu98Hdz1l_lcSZ2rY60Ajjk9U1c': Stayonline.result['code'],
        }

        data = {
            'id': id,
            'ref': '',
        }

        response = requests.post('https://stayonline.pro/ajax/linkView.php', cookies=cookies, headers=headers,
                                 data=data)
        return json.loads(response.content)['data']['value']

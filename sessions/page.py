# -*- coding: utf-8 -*-
import requests

import base64
"""
from PIL import Image
import pytesseract
"""

import requests
from bs4 import BeautifulSoup
from sessions import MyHttp, Agent, Stayonline
from urllib.parse import urlparse


class Page:

    def __init__(self, page: str):
        self.page = page
        self.site_headers = Agent.headers(host="cb01.poker",
                                          refer='www.google.com',
                                          document='document', secfetchSite='none')
        self.filehost_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.10; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'en-US,en;q=0.5'
        }

    async def get_url(self, url: str, headers=None, proxy=None):
        if not headers:
            headers = self.filehost_headers
        async with MyHttp(headers=headers, cache_dir="Movie", cache=False) as my_http:
            return await my_http.get(url=url, proxy=proxy)

    async def get_home_urls(self) -> []:
        home_body, _ = await self.get_url(url=self.page, headers=self.site_headers)
        soup = BeautifulSoup(home_body, 'html.parser')
        # Trova tutti gli elementi h3 con classe 'card-title'
        h3_elements = soup.find_all('h3', class_='card-title')
        return [h3.find('a')['href'] for h3 in h3_elements if h3.find('a') and 'href' in h3.find('a').attrs]

    async def get_video_url(self, url: str):
        urls = []
        video, _ = await self.get_url(url=url, headers=self.site_headers)
        soup = BeautifulSoup(video, 'html.parser')
        td_elements = soup.find_all('td')
        for td in td_elements:
            link = td.find('a')
            if link:
                if link.get('target') == '_blank':
                    text = link.get_text()
                    if text.lower() in ['maxstream', 'mixdrop']:
                        href = link.get('href')
                        urls.append(href)
        return urls

    def best_resolution(self, video_urls: list, host_name: str) -> str:
        best_url = None
        for search in video_urls:
            if host_name.lower() in search.lower():
                best_url = search
        return best_url

    def mixdrop_url(self, stayonline_url: str) -> str:
        # sudo apt-get install tesseract-ocr

        mixdrop_url = Stayonline.get_url(url=stayonline_url)
        parse_path = urlparse(mixdrop_url).path.split('/')[2]
        mixdrop_player_url = f"https://mixdrop.ag/e/{parse_path}"
        return mixdrop_player_url

    # Maxstream
    """
    async def uprot_url(self, uprot_url: str) -> str:
        # https://developers.cloudflare.com/fundamentals/reference/policies-compliances/cloudflare-cookies/

        html_source, _ = await self.get_url(url=uprot_url)
        start_index = html_source.find('base64,') + len('base64,')
        end_index = html_source.find('"', start_index)
        img_base64 = html_source[start_index:end_index]
        # Decodifica dell'immagine
        img_data = base64.b64decode(img_base64)
        img = Image.open(BytesIO(img_data))
        # Utilizza pytesseract per estrarre il testo dall'immagine
        text = pytesseract.image_to_string(img)
        # Stampa il testo estratto


        url = uprot_url  # Sostituisci con l'endpoint corretto di Cloudflare
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Origin": "https://uprot.net",  # Sostituisci con l'origin corretto
            "Connection": "keep-alive",
            "Referer": uprot_url,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }

        # Formato payload (esempio)
        payload = {
            "number": text.strip(),
        }

        # Invia la richiesta POST
        response = requests.post(url, headers=headers, json=payload)

        # Stampa la risposta dal server
        print(response.status_code)
        #print(response.text)
        cookies = response.cookies
        phpsessid_value = ''
        for cookie in cookies:
            if cookie.name == 'PHPSESSID':
                phpsessid_value = cookie.value
                print(phpsessid_value)
                break

        cookies = {
            "PHPSESSID": phpsessid_value
        }

        response = requests.post(url, headers=headers, cookies=cookies)

        # Stampa la risposta dal server
        print(response.status_code)
        print(response.text)
    """
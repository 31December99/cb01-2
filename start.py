# -*- coding: utf-8 -*-

import asyncio
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from sessions import MyHttp, Agent, Stayonline, true_link


class Page:

    def __init__(self, page: str):
        self.page = page
        self.site_headers = Agent.headers(host="cb01.church",
                                          refer='www.google.com',
                                          document='document', secfetchSite='none')
        self.filehost_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.10; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'en-US,en;q=0.5'
        }

    async def get_url(self, url: str, headers=None):
        if not headers:
            headers = self.filehost_headers
        async with MyHttp(headers=headers, cache_dir="Movie", cache=False) as my_http:
            return await my_http.get(url)

    async def get_home_urls(self) -> []:
        home_body = await self.get_url(url=self.page, headers=self.site_headers)
        soup = BeautifulSoup(home_body, 'html.parser')
        # Trova tutti gli elementi h3 con classe 'card-title'
        h3_elements = soup.find_all('h3', class_='card-title')
        return [h3.find('a')['href'] for h3 in h3_elements if h3.find('a') and 'href' in h3.find('a').attrs]

    async def get_video_url(self, url: str):
        urls = []
        video = await self.get_url(url=url, headers=self.site_headers)
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
        mixdrop_url = Stayonline.get_url(url=stayonline_url)
        parse_path = urlparse(mixdrop_url).path.split('/')[2]
        mixdrop_player_url = f"https://mixdrop.ag/e/{parse_path}"
        return mixdrop_player_url


async def start():
    # Scelgo la Pagina e ottengo tutti gli urls all'interno
    page_n = input("Scegli una pagina...[0-2300] ")
    page = Page(page=f"https://cb01.church/page/{page_n}/")
    videos_home = await page.get_home_urls()

    for index, url in enumerate(videos_home):
        print(f"{index}) {url}")

    # Scelgo la home page del film e ottengo tutti gli urls mixdrop all'interno
    page_url = input("Scegli il film digitando il numero corrispondente - ")

    video_urls = await page.get_video_url(videos_home[int(page_url)])
    best_resolution_url = page.best_resolution(video_urls, 'stayonline')

    if best_resolution_url:
        mixdrop_player_url = page.mixdrop_url(stayonline_url=best_resolution_url)
        respond = await page.get_url(url=mixdrop_player_url)
        download_url = true_link(respond)
        print(download_url)


if __name__ == "__main__":
    asyncio.run(start())

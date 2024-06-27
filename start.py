import asyncio
import time
import traceback
import logging
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from sessions import Agent, session_cached, MyHttp, Cache, Stayonline

# Configurazione del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Page:
    # Creo un nuovo Agent
    headers = Agent.headers(host="cb01.church",
                            refer='www.google.com',
                            document='document', secfetchSite='none')

    def __init__(self, type: str, urls=None):
        self.urls = urls
        self.type = type

    async def download_url(self, url: str, my_http: MyHttp):
        return await my_http.get(url)

    async def find_all(self):
        async with MyHttp(headers=Page.headers, cache_dir=self.type, cache=True) as my_http:
            my_http.load_cache()
            tasks = [self.download_url(url, my_http) for url in self.urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Task {i} error: {result} ")
                    logger.error(traceback.format_exc())
            logger.info("Closing...")
            my_http.save_cache()

    async def find_page(self, url: str):
        async with session_cached.MyHttp(headers=Page.headers, cache_dir=self.type, cache=True) as my_http:
            await self.download_url(url, my_http)
        print("Closing...")

    def get_urls_page(self, page_url: str):
        pass


class Cb01(Page):

    def __init__(self, urls: list, type: str):
        super().__init__(type, urls)
        self.cache = Cache(self.type)

    def get_urls_page(self, page_url: str) -> []:
        """ ottiene tutti gli urls della pagina """
        urls = []
        video_cached = self.cache.get_cache(page_url)
        # Parsing della pagina
        soup = BeautifulSoup(video_cached.decode(), 'html.parser')

        # Trova tutti gli elementi h3 con classe 'card-title'
        h3_elements = soup.find_all('h3', class_='card-title')
        for h3 in h3_elements:
            # Trova il tag 'a' all'interno del tag 'h3'
            a_tag = h3.find('a')
            if a_tag and 'href' in a_tag.attrs:
                urls.append(a_tag['href'])
        return urls

    async def get_urls_video(self, url: str):
        """ ottiene tutti gli urls del video """
        urls = []
        video_cached = self.cache.get_cache(url)
        soup = BeautifulSoup(video_cached.decode(), 'html.parser')
        td_elements = soup.find_all('td')
        for td in td_elements:
            link = td.find('a')
            if link:
                if link.get('target') == '_blank':
                    text = link.get_text()
                    if text.lower() in ['maxstream', 'mixdrop']:
                        href = link.get('href')  # Ottenere l'attributo 'href' del link
                        urls.append(href)
        return urls


async def start():
    # Timer
    start_timer = time.time()
    # Crea un indice di tutte le pagine principali contenenti i video
    pages_url = [f"https://cb01.church/page/{number}/" for number in range(1, 300)]
    # Avvia il download di tutte le pagine
    all_home_pages = Cb01(urls=pages_url, type='Movie')
    # cache di tutte le pagine principali home
    await all_home_pages.find_all()
    # print(f"FINE {time.time() - start_timer}")

    # Timer
    page_n = input("Scegli una pagina -> ")
    # Scelgo la Pagina e ottengo tutti gli urls all'interno
    page_urls = all_home_pages.get_urls_page(f"https://cb01.church/page/{page_n}/")
    page = Cb01(urls=page_urls, type=f"Page{page_n}")
    # cache della Pagina
    await page.find_all()
    for page_url in page_urls:
        video_url = await page.get_urls_video(page_url)
        parsed_uri = urlparse(page_url)
        print(f"\n{parsed_uri.path.replace('/', '').replace('-', ' ').upper()}\n{video_url}")
        final_url = Stayonline.get_url(url=video_url[2])
        input(f"-> URL[{final_url}]\nPremi invio per continuare ")

if __name__ == "__main__":
    asyncio.run(start())

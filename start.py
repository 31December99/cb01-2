# -*- coding: utf-8 -*-
import asyncio
import sys

from sessions import true_link, Page, Split
from download import Downloader


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

    # Ottengo il link stayonline HD
    if best_resolution_url:
        mixdrop_player_url = page.mixdrop_url(stayonline_url=best_resolution_url)
        print(f"{mixdrop_player_url}...Attendi generazione dei link per il download")

        proxy_group = ['http://104.207.52.23:3128', 'http://104.167.25.171:3128',
                       'http://104.207.51.28:3128', 'http://104.167.26.142:3128',
                       'http://104.167.26.202:3128', 'http://104.167.31.121:3128',
                       'http://104.167.29.55:3128', 'http://104.207.36.135:3128',
                       'http://104.167.31.88:3128', 'http://104.167.29.54:3128',
                       None]  # None = Ip corrente

        download_group = []
        php_sessid_group = []

        for proxy_ip in proxy_group:
            respond, php_sessid = await page.get_url(url=mixdrop_player_url, proxy=proxy_ip)
            download_url = true_link(respond)
            download_group.append(download_url)
            php_sessid_group.append(php_sessid)
            if download_url:
                print(f"Real link:{download_url}  Sessid:{php_sessid}")
            else:
                print("Url non disponibile")
                sys.exit()

        # Splitto il file in tre parti uno per proxy e passi i gli url delivery
        # infine richiedo con HEAD il content-lenght e divido il size per il numero di parti richieste
        sp = Split(download_group[-1])
        headers_ranges = sp.get_ranges(parts=len(proxy_group), download_group=download_group,
                                       proxy_group=proxy_group, php_sessid_group=php_sessid_group)

        # Passo tutto al downloader
        video = Downloader(playlist=headers_ranges, file_name="Test3", media='VIDEO')
        video.start()
        video.close()


if __name__ == "__main__":
    asyncio.run(start())

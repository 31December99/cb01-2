# -*- coding: utf-8 -*-
import asyncio
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

        proxy_group = ['http://104.207.59.91:3128', 'http://104.207.42.108:3128',
                       'http://104.207.49.179:3128', 'http://104.207.58.16:3128',
                       'http://104.207.52.104:3128', 'http://104.207.60.98:3128',
                       'http://104.207.47.249:3128', 'http://104.207.44.136:3128',
                       'http://104.207.37.94:3128', 'http://104.167.25.177:3128',
                       None]  # None = Ip corrente

        # Url stayonline con proxy #0
        respond, php_sessid0 = await page.get_url(url=mixdrop_player_url, proxy=proxy_group[0])
        download_url0 = true_link(respond)

        # Url stayonline con proxy #1
        respond, php_sessid1 = await page.get_url(url=mixdrop_player_url, proxy=proxy_group[1])
        download_url1 = true_link(respond)

        # Url stayonline con proxy #2
        respond, php_sessid2 = await page.get_url(url=mixdrop_player_url, proxy=proxy_group[2])
        download_url2 = true_link(respond)

        # Url stayonline con proxy #3
        respond, php_sessid3 = await page.get_url(url=mixdrop_player_url, proxy=proxy_group[3])
        download_url3 = true_link(respond)

        # Url stayonline con proxy #4
        respond, php_sessid4 = await page.get_url(url=mixdrop_player_url, proxy=proxy_group[4])
        download_url4 = true_link(respond)

        # Url stayonline con proxy #5
        respond, php_sessid5 = await page.get_url(url=mixdrop_player_url, proxy=proxy_group[5])
        download_url5 = true_link(respond)

        # Url stayonline con proxy #6
        respond, php_sessid6 = await page.get_url(url=mixdrop_player_url, proxy=proxy_group[6])
        download_url6 = true_link(respond)

        # Url stayonline con proxy #7
        respond, php_sessid7 = await page.get_url(url=mixdrop_player_url, proxy=proxy_group[7])
        download_url7 = true_link(respond)

        # Url stayonline con proxy #8
        respond, php_sessid8 = await page.get_url(url=mixdrop_player_url, proxy=proxy_group[8])
        download_url8 = true_link(respond)

        # Url stayonline con proxy #9
        respond, php_sessid9 = await page.get_url(url=mixdrop_player_url, proxy=proxy_group[9])
        download_url9 = true_link(respond)

        # Url stayonline con proxy #10
        respond, php_sessid10 = await page.get_url(url=mixdrop_player_url, proxy=proxy_group[10])
        download_url10 = true_link(respond)

        # Url stayonline con proxy #11
        respond, php_sessid11 = await page.get_url(url=mixdrop_player_url)
        download_url11 = true_link(respond)

        download_group = [download_url0, download_url1, download_url2, download_url3, download_url4,
                          download_url5, download_url6, download_url7, download_url8, download_url9,
                          download_url10, download_url11]

        php_sessid_group = [php_sessid0, php_sessid1, php_sessid2, php_sessid3, php_sessid4,
                            php_sessid5, php_sessid6, php_sessid7, php_sessid8, php_sessid9,
                            php_sessid10, php_sessid11]

        # Splitto il file in tre parti uno per proxy e passi i gli url delivery
        # infine richiedo con HEAD il content-lenght e divido il size per il numero di parti richieste
        sp = Split(download_url11)
        headers_ranges = sp.get_ranges(parts=11, download_group=download_group,
                                       proxy_group=proxy_group, php_sessid_group=php_sessid_group)

        # Passo tutto al downloader
        video = Downloader(playlist=headers_ranges, file_name="Test3", media='VIDEO')
        video.start()
        video.close()


if __name__ == "__main__":
    asyncio.run(start())

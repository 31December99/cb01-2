# -*- coding: utf-8 -*-
import requests


class Split:
    """ crea un elenco di range basati content-lengh diviso per numeri di parts """

    def __init__(self, url: str):
        self.url = url

    def get_size(self, parts: int) -> []:
        """ Ottengo il range per ogni richiesta http """

        # Ottengo il size del file
        response = requests.head(self.url)
        file_size = int(response.headers['Content-Length'])
        # Ottengo il size di ogni chunk e un eventuale rimanenza se inferiore a parts
        chunk_size = file_size // parts
        remainder = file_size % parts

        # creo una lista con all'interno ogni tupla ( range)
        ranges = []
        for i in range(parts):
            start = i * chunk_size
            # L'ultima rquesta terrà conto anche del residuo o remainder
            end = start + chunk_size - 1 if i < parts - 1 else start + chunk_size + remainder - 1
            ranges.append((start, end))
        return ranges

    def get_ranges(self, parts: int, download_group: list, proxy_group: list, php_sessid_group: list):
        ranges = self.get_size(parts)

        headers_ranges = [{'Range': f'bytes={range_tuple[0]}-{range_tuple[1]}',
                           'url': '', 'proxy': '', 'Cookie': ''} for range_tuple in ranges]

        for header, url in zip(headers_ranges, download_group):
            header['url'] = url

        for header, proxy in zip(headers_ranges, proxy_group):
            header['proxy'] = proxy

        for header, php_sessid in zip(headers_ranges, php_sessid_group):
            header['Cookie'] = f'PHPSESSID={php_sessid}'

        #Stampa
        print("-")
        for range in headers_ranges:
            print(range)

        return headers_ranges

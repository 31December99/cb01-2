# -*- coding: utf-8 -*-
import os
from queue import Queue
from urllib.parse import urlparse

from .proxy import Proxy, MAX_THREAD


class Downloader:
    """
        Crea i threads per il download
    """

    def __init__(self, playlist: [], file_name: str, media: str, key=False):
        self.playlist: [] = playlist
        self.key: bool = key
        self.queue: Queue = Queue()
        self.threads: list = []
        self.file_name: str = file_name
        self.media: str = media

    def start(self):

        # Ritorna se playlist non disponibile
        if not self.playlist:
            return

        # Ottiene il nome del file da un url qualasiasi della lista
        parsed_uri = urlparse(self.playlist[0]['url'])
        self.file_name = parsed_uri.path.split('/')[-1]

        # Crea la cartella download in home/user
        home_folder = os.path.expanduser("~")
        file_path = os.path.join(home_folder, "CB01_Downloads", self.file_name, self.media)

        # Salva tutti i segments.uri in una coda safe-thread
        for index, items in enumerate(self.playlist):
            self.queue.put((items['url'], items['Range'], items['proxy'], items['Cookie'], index))

        # Creo i threads: ogni thread legge dalla coda e processa un url.
        # Terminato di processare l'url , leggerà nuovamente dalla coda è cos' via.
        # Finchè tutti i thread non processeranno tutti gli url della coda
        threads = []
        print()

        # Ho a disposizione proxy pari a MAX_PROXY. Utilizzerò un gruppo di ip massimo pari a MAX_THREAD
        for _ in range(MAX_THREAD):
            thread = Proxy(coda=self.queue, file_path=file_path, key=self.key)
            thread.start()
            self.threads.append(thread)

        for thread in threads:
            thread.join()

        # Attendo la fine di tutto il processo
        self.queue.join()
        return file_path

    def close(self):
        for thread in self.threads:
            thread.stop_writing()

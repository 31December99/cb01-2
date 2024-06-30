# -*- coding: utf-8 -*-
import os
import threading
import random
import warnings
import concurrent.futures
import queue
import requests
from sessions import Agent
from urllib.parse import urlparse

""" SSL off """
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

MAX_PROXY = 100
MAX_THREAD = 11
MAX_INIT_RND = MAX_PROXY - MAX_THREAD
# Test header in locale 127.0.0.1 con test_headers.py
TEST_HEADER = False
proxy_queue = queue.Queue()


class Proxy(threading.Thread):
    """
    - Ogni proxy un thread
    - Processa il prossimo url in run()
    """
    proxy_lock = threading.Lock()
    proxy_index = random.randrange(0, MAX_INIT_RND)
    session = requests.Session()

    def __init__(self, coda: queue, file_path: str, key: bool):
        super(Proxy, self).__init__()
        self.headers = None
        self.queue = coda
        self.key: bool = key
        self.folder = file_path
        self.user_agent = None
        self.proxy_ip = None
        self.stop_event = threading.Event()
        self.write_queue: queue = queue.Queue()
        self.executor: concurrent = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        threading.Thread(target=self.process_write_queue, daemon=True).start()
        self.results = {}
        self.next_headers()

        if not os.path.exists(file_path):
            os.makedirs(file_path)

    def next_headers(self):
        # L'ordine degli headers è importante
        self.headers = Agent.headers(host="s-delivery31.mxcontent.net",
                                     refer='mixdrop.ms', secfetchSite='cross-site',
                                     document='document', mode='navigate')

    def run(self):
        """ threading.Thread"""
        while not self.queue.empty():
            url, header_range, proxy, cookie, index = self.queue.get()

            try:
                content, segment_filename = self.download_url(url, header_range, proxy, cookie)
                if content:
                    self.write_queue.put((content, segment_filename, index))
            finally:
                self.queue.task_done()

    def download_url(self, url: str, header_range: str, proxy_url: str, cookie: str):
        """ creo un nuovo url con il nuovo proxy. Timeout 30 secondi"""

        parsed_uri = urlparse(url)
        # aggiorno l'header con un nuovo host che corrisponde al net-loc dell'url scws
        self.headers['host'] = parsed_uri.netloc
        self.headers.update({'Range': header_range})
        self.headers.update({'Cookie': cookie})

        filename = parsed_uri.path.split('/')[-1]
        # print(f"HEADERS DOWNLOAD URL {self.headers}")

        try:
            response = Proxy.session.get(url, headers=self.headers, stream=True,
                                         proxies={'http': proxy_url, 'https': proxy_url}, timeout=30, verify=False)

            if response.status_code == 206:
                print(f"[{threading.current_thread().name} {response.status_code}] -> {url} {proxy_url}")
                return response, filename
            else:
                print(f"[{response.status_code}] {proxy_url} -> {url}")
                return '', ''
        except Exception as e:
            print(f"[ * EXCPT * {e}] {proxy_url} -> {url}")
            return '', ''

    def process_write_queue(self):
        while not self.stop_event.is_set():
            try:
                while not self.write_queue.empty():
                    segment_content, ts_filename, index = self.write_queue.get()
                    if segment_content:
                        self.write_to_file(segment_content, ts_filename, index)
            except queue.Empty:
                pass
            finally:
                threading.Event().wait(1)

    def write_to_file(self, response: requests, ts_filename: str, index: int):
        try:
            # print(f"[DOWNLOAD] {self.folder} -> {ts_filename}")
            with open(os.path.join(self.folder, f"{str(index).zfill(4)}_{ts_filename}"), 'wb') as file:
                for chunk in response.iter_content(chunk_size=2048):
                    file.write(chunk)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.write_queue.task_done()
            if not self.write_queue.empty():
                self.executor.submit(self.process_write_queue)

    def stop_writing(self):
        # Attende la fine della coda
        self.write_queue.join()
        # fine processo write_queue
        self.stop_event.set()
        # chiude thread
        self.executor.shutdown(wait=True)
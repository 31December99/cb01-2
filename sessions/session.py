# -*- coding: utf-8 -*-
import asyncio
import warnings
from aiohttp import TCPConnector, ClientSession, ClientTimeout
from aiocache import SimpleMemoryCache
from aiocache.serializers import BaseSerializer
import diskcache


class Cache:
    """ Carico la cache in locale"""

    def __init__(self, cache_folder: str = './cache'):
        self.disk_cache = diskcache.Cache(cache_folder)

    def get_cache(self, url: str):
        cached_data = self.disk_cache.get(url)
        if cached_data:
            return cached_data
        return None


class CustomJsonSerializer(BaseSerializer):
    def loads(self, value: bytes) -> bytes:
        # nessuna conversione per il momento
        return value

    def dumps(self, value: bytes) -> bytes:
        # nessuna conversione per il momento
        return value


class MyHttp:
    """Classe per gestire chiamate http con cache persistente"""

    warnings.filterwarnings('ignore', message='Unverified HTTPS request')
    timeout = ClientTimeout(total=30)

    def __init__(self, headers: dict, cache=False, cache_dir: str = './cache'):
        self.session = None
        self.cache = cache
        self.headers = headers
        self.semaphore = asyncio.Semaphore(200)
        self.memory_cache = SimpleMemoryCache(serializer=CustomJsonSerializer(), ttl=300)
        self.disk_cache = diskcache.Cache(cache_dir)

    async def __aenter__(self):
        self.session = ClientSession(timeout=self.timeout, connector=TCPConnector(verify_ssl=False, limit=200),
                                     headers=self.headers)
        self.load_cache()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()
        self.save_cache()

    def get_session(self):
        return self.session

    async def get(self, url: str, proxy=None) -> (str, str):
        response = await self.session.get(url=url, proxy=proxy)
        # print(f"[cache {self.cache}] -> {url} [{response.status}]")
        if response.status == 200 and self.cache:
            body = await response.text()
            await self.memory_cache.set(url, body)
            return body
        elif response.status == 200:
            cookies = response.cookies
            if cookies:
                php_sess_id = cookies.get('PHPSESSID').value
            else:
                php_sess_id = ''
            return await response.text(), php_sess_id
        else:
            return ''

    async def get_content(self, url: str) -> str:
        response = await self.session.get(url)
        if response.status == 200:
            return await response.text()
        else:
            return ''

    def save_cache(self):
        """ Passa dalla ram al disco """
        for key in self.memory_cache._cache.keys():
            value = self.memory_cache._cache[key]
            self.disk_cache[key] = value

    def load_cache(self):
        """ carica dall disco alla ram """
        for key in self.disk_cache:
            self.memory_cache._cache[key] = self.disk_cache[key]

#!/usr/bin/env python3
""" Module for function get_page  """
import redis
import functools
import requests

redis_store = redis.Redis()


def access_count(fn):
    """  track how many times a particular URL was accessed """
    @functools.wraps(fn)
    def wrapper(url):
        """ caches requeted url """
        cache_key = f"url:+{url}"
        cached_content = redis_store.get(cache_key)
        if cached_content:
            return cached_content.decode()
        content = fn(url)
        key = "count:" + url
        redis_store.set(cache_key, content)
        redis_store.incr(key)
        redis_store.expire(cache_key, 10)
        return content
    return wrapper


@access_count
def get_page(url: str) -> str:
    """ fetches the HTML content of a particular URL and returns it """
    return requests.get(url).text

#!/usr/bin/env python3
""" Module for class Cache implementing some storage cache functionalities """

from typing import Callable, Union, Optional, Any
import uuid
import redis
import functools


def replay(function: Callable) -> None:
    """  display the history of calls of a particular function. """
    r = redis.Redis()
    key = function.__qualname__
    input_key = key + ":inputs"
    output_key = key + ":outputs"
    count = r.get(key)
    try:
        count = int(count.decode())
    except Exception:
        count = 0
    print(f"{key} was called {count} times")
    inputs = r.lrange(input_key, 0, -1)
    outputs = r.lrange(output_key, 0, -1)
    for inpt, output in zip(inputs, outputs):
        try:
            result_1 = inpt.decode()
        except Exception:
            result_1 = ""
        try:
            result_2 = output.decode()
        except Exception:
            result_2 = ""
        print(f"{key}(*{result_1}) -> {result_2}")


def call_history(method: Callable) -> Callable:
    """ keeps record of a methods input parameters """
    key = method.__qualname__

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """ adds parameters to database list """
        input_key = key + ":inputs"
        output_key = key + ":outputs"
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, result)
        return result
    return wrapper


def count_calls(method: Callable) -> Callable:
    """ keeps record of how many times methods of Cache class are called """
    key = method.__qualname__

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """ incremets count of Cache class method calls """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """ A class that models storage cache """
    def __init__(self):
        """ Constructor for an instance of a cache object """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Generates random string as key for data value to store in database
        and returns the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ Fetche value associated with a key and applies optionl funtion to
        it """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ automatically parametrize Cache.get with the correct conversion """
        return str(self.get(key, fn=bytes.decode))

    def get_int(self, key: str) -> int:
        """ automatically parametrize Cache.get with the correct conversion """
        try:
            value = int(self.get(key, fn=bytes.decode))
        except Exception:
            value = 0
        return value

import redis
import json
import os
from abc import ABCMeta, abstractmethod


class KVSBase(metaclass=ABCMeta):
    def __init__(self, prefix: str):
        self.__prefix = prefix

    def real_key(self, key) -> str:
        return '{:s}:{:s}'.format(self.__prefix, key)

    @property
    def prefix(self) -> str:
        return self.__prefix

    @abstractmethod
    def __getitem__(self, key: str) -> object:
        pass

    @abstractmethod
    def __setitem__(self, key: str, value: object) -> object:
        pass

    @abstractmethod
    def __delitem__(self, key: str):
        pass

    @abstractmethod
    def __iter__(self) -> object:
        pass


class Redis(KVSBase):
    def __init__(self, prefix: str, connection_pool: redis.ConnectionPool):
        KVSBase.__init__(self, prefix)
        self.__redis = redis.Redis(connection_pool=connection_pool)

    def __delitem__(self, key):
        if self.__redis.delete(self.real_key(key)) == 0:
            raise KeyError

    def __getitem__(self, key):
        value = self.__redis.get(self.real_key(key))

        if value is None:
            raise KeyError

        return json.loads(value.decode('utf-8'))

    def __setitem__(self, key, value):
        self.__redis.set(self.real_key(key), json.dumps(value))
        return value

    def __iter__(self) -> object:
        return RedisIter(self)

    @property
    def redis(self) -> redis.Redis:
        return self.__redis


class RedisIter(object):
    def __init__(self, r: Redis):
        self.__redis = r
        self.__keys = [x.decode('utf-8').replace(r.prefix + ':', '') for x in r.redis.keys(r.prefix + '*')]

    def __next__(self):
        if self.__keys:
            key = self.__keys.pop()
            return key, self.__redis[key]
        else:
            raise StopIteration


class Dict(KVSBase):
    def __init__(self, prefix: str):
        KVSBase.__init__(self, prefix)
        self.__dict = {}

    def __delitem__(self, key):
        del (self.__dict[self.real_key(key)])

    def __getitem__(self, key):
        return self.__dict[self.real_key(key)]

    def __setitem__(self, key, value):
        self.__dict[self.real_key(key)] = value

    def __iter__(self):
        return DictIter(self)

    @property
    def dict(self):
        return self.__dict


class DictIter(object):
    def __init__(self, d: Dict):
        self.__dict = d
        self.__keys = [x.replace(d.prefix + ':', '') for x in d.dict.keys()]

    def __next__(self):
        if self.__keys:
            key = self.__keys.pop()
            return key, self.__dict[key]
        else:
            raise StopIteration


class KVSManager(object):
    def __init__(self):
        self.redis_connection_pool = None

        redis_host = None
        redis_port = None

        try:
            redis_host = os.environ['REDIS_HOST']
            redis_port = os.environ['REDIS_PORT']
        except KeyError:
            pass

        if redis_host and redis_port:
            self.redis_connection_pool = redis.ConnectionPool(host=redis_host, port=redis_port)

    def get_kvs(self, prefix: str) -> KVSBase:
        if self.redis_connection_pool:
            return Redis(prefix, self.redis_connection_pool)
        else:
            return Dict(prefix)

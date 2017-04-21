import pytest
import redis

from app.kvs import Redis, Dict


@pytest.fixture(scope='class', params=[
    Redis(prefix='subot:test', connection_pool=redis.ConnectionPool(host='localhost', port=6379)),
    Dict(prefix='subot:test')
])
def kvs(request):
    return request.param


class TestKVS(object):
    def test_set(self, kvs):
        kvs['set test'] = 'set test value'

    def test_del(self, kvs):
        kvs['del test'] = 'del test value'
        del (kvs['del test'])

    def test_get(self, kvs):
        kvs['get test'] = 'get test value'
        assert kvs['get test'] == 'get test value'

    def test_get_invalid_key(self, kvs):
        with pytest.raises(KeyError):
            _ = kvs['invalid key']

    def test_del_invalid_key(self, kvs):
        with pytest.raises(KeyError):
            del (kvs['invalid key'])

    def test_iter(self, kvs):
        original = {'a': 1, 'b': 2}
        result = {}

        for key, value in original.items():
            kvs[key] = value

        for key, value in kvs:
            result[key] = value

        assert all(item in result for item in original)

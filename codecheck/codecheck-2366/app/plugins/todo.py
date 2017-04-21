import os
from redis import Redis

from . import PluginBase

__all__ = ['ToDo']


class ToDo(PluginBase):
    def __init__(self):
        self._redis = Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']))
        self._redis_name = 'subot:todo'

    def execute(self, args):
        if len(args) < 1:
            raise ValueError('wrong number of arguments are given')

        command = args[0]

        if command == 'list':
            return self.__list_task()

        elif command == 'add' and len(args) >= 3:
            title = args[1]
            description = ' '.join(args[2:])
            return self.__add_task(title, description)

        elif command == 'delete' and len(args) == 2:
            title = args[1]
            return self.__delete_task(title)

        else:
            raise RuntimeError('unknown command')

    def __add_task(self, title, description):
        if not self._redis.hexists(self._redis_name, title):
            self._redis.hset(self._redis_name, title, description)
            return 'todo added'

        else:
            raise RuntimeError('todo already exists')

    def __delete_task(self, title):
        if self._redis.hdel(self._redis_name, title):
            return 'todo deleted'
        else:
            raise RuntimeError('todo not found')

    def __list_task(self):
        result = []

        for title, description in self._redis.hgetall(self._redis_name).items():
            result.append('{:s} {:s}'.format(title.decode(), description.decode()))

        if not result:
            return 'todo empty'

        return '\n'.join(result)

    def help(self):
        return '(add|delete|list) args...\n' \
               ' - add title description... : Add task\n' \
               ' - delete title : Delete task which have the title\n' \
               ' - list : Print all tasks'

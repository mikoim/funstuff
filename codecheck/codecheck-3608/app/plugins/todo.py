from . import PluginBase

__all__ = ['ToDo']


class ToDo(PluginBase):
    def __init__(self, kvs):
        super().__init__(kvs)

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
        if title not in self.kvs:
            self.kvs[title] = description
            return 'todo added'
        else:
            raise RuntimeError('todo already exists')

    def __delete_task(self, title):
        try:
            del (self.kvs[title])
            return 'todo deleted'
        except KeyError:
            raise RuntimeError('todo not found')

    def __list_task(self):
        result = []

        for title, description in self.kvs:
            result.append('{:s} {:s}'.format(title, description))

        if not result:
            return 'todo empty'

        return '\n'.join(result)

    def help(self):
        return """[add|delete|list] [args...]
  - add [title] [description...] : Add task with the title
  - delete [title] : Delete task which have the title
  - list : Print all tasks

ex)
  > todo add foo bar
  todo added

  > todo delete foo
  todo deleted

  > todo list
  foo bar
"""

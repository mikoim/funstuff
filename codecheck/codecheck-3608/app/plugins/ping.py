from . import PluginBase

__all__ = ['Ping']


class Ping(PluginBase):
    def execute(self, args):
        return 'pong'

    def help(self):
        return """
Just say "pong".

ex)
  > ping
  pong
"""

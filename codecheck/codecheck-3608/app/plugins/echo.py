from . import PluginBase

__all__ = ['Echo']


class Echo(PluginBase):
    def execute(self, args):
        return ' '.join(args)

    def help(self):
        return """[text...]
echo says a line of text.

ex)
  > echo hoge
  hoge
"""

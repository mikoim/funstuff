from . import PluginBase

__all__ = ['Help']


class Help(PluginBase):
    def __init__(self, kvs, plugins):
        """
        :type plugins: dict
        """
        super().__init__(kvs)
        self._plugins = plugins

    def help(self):
        return '\n' \
               'Print all installed plugin with help string.'

    def execute(self, args):
        result = '===== Plugins =====\n'

        result += '\n{:d} plugins are installed.'.format(len(self._plugins))

        for alias, plugin in self._plugins.items():
            result += '\n\n* {:s} {:s}'.format(alias, plugin.help())

        return result

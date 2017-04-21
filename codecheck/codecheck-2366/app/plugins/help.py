from . import PluginBase

__all__ = ['Help']


class Help(PluginBase):
    def __init__(self, plugins):
        """
        :type plugins: dict
        """
        self._plugins = plugins

    def help(self):
        return '\n' \
               'Print all installed plugin with help string.'

    def execute(self, args):
        result = '===== Plugins ====='

        for alias, plugin in self._plugins.items():
            result += '\n\n{:s} {:s}'.format(alias, plugin.help())

        result += '\n\n{:d} plugins are installed.'.format(len(self._plugins))

        return result

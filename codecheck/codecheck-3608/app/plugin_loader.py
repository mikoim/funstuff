import os
import re
from importlib import import_module
from os import path

from .kvs import KVSManager


class PluginLoader:
    @staticmethod
    def get_plugins(kvsm: KVSManager):
        src = path.dirname(path.abspath(__file__)) + '/plugins'

        plugin_regex = re.compile('^(?!_+)\w+\.py$')
        plugins_py = [x.split('.')[0] for x in os.listdir(src) if plugin_regex.match(x)]

        plugins = {}

        import_module('app.plugins')

        for plugin_file in plugins_py:
            plugin = import_module('.' + plugin_file, 'app.plugins')
            if plugin_file != 'help':
                plugins[plugin_file] = getattr(plugin, plugin.__all__[0])(kvsm.get_kvs('subot:' + plugin_file))
            else:
                plugins[plugin_file] = getattr(plugin, plugin.__all__[0])(None, plugins)

        return plugins

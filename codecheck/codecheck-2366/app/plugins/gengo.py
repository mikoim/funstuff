from datetime import datetime

import rfGengou

from . import PluginBase

__all__ = ['Gengo']


class Gengo(PluginBase):
    def execute(self, args):
        if len(args) == 0:
            target = datetime.now()
        elif len(args) == 1:
            target = datetime.strptime(args[0], '%Y/%m/%d')
        else:
            raise ValueError('wrong number of arguments are given')

        return '{:s}{:d}年{:d}月{:d}日'.format(*rfGengou.s2g(target))

    def help(self):
        return '(yyyy/mm/dd)\n' \
               'Convert from string to Japanese Gengo.\n' \
               'If string is not given, use current time.'

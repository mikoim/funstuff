from datetime import datetime

from pytz import timezone, UnknownTimeZoneError

from . import PluginBase

__all__ = ['TZ']


class TZ(PluginBase):
    def __init__(self):
        self._format = ''

    def execute(self, args):
        if len(args) != 1:
            raise ValueError('wrong number of arguments are given')

        try:
            tz = timezone(args[0])
        except UnknownTimeZoneError:
            raise ValueError('unknown time zone')

        now_utc = datetime.now(timezone('UTC'))
        now_target = now_utc.astimezone(tz)

        return '{:s} : {:s}'.format(tz.zone, now_target.isoformat())

    def help(self):
        return 'timezone \n' \
               'Convert current time to specific timezone.'

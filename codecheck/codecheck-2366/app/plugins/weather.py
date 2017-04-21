import os
from pyowm import OWM

from . import PluginBase

__all__ = ['Weather']


class Weather(PluginBase):
    def __init__(self):
        self._owm = OWM(os.environ['OWM_API_KEY'])

    def execute(self, args):
        if len(args) != 1:
            raise ValueError('wrong number of arguments are given')

        location = args[0]

        result = ''
        for weather in self._owm.daily_forecast(location, 7).get_forecast():
            result += '{:s} {:s}\n'.format(weather.get_reference_time('iso'), weather.get_status())

        return result

    def help(self):
        return 'location\n' \
               'Print current weather observations and forecast'

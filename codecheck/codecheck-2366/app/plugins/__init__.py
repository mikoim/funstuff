from abc import ABCMeta, abstractmethod


class PluginBase(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, args):
        """
        Execute command and return result

        :rtype: str
        """
        pass

    @abstractmethod
    def help(self):
        """
        Return help string

        :rtype: str
        """
        pass

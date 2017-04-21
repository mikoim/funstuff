from abc import ABCMeta, abstractmethod


class PluginBase(metaclass=ABCMeta):
    def __init__(self, kvs):
        self.kvs = kvs

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

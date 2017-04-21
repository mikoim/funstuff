import re


class LookAndSay(object):
    def __init__(self, stop, length=None):
        self.__stop = stop
        self.__re = re.compile('(1+|2+|3+)')
        if type(length) is int:
            self.__length = int(length * 1.6)
        else:
            self.__length = None
        self.__length_ret = length

    def __iter__(self):
        self.__seq = '1'
        self.__step = 0
        return self

    def __next__(self):
        if self.__step > self.__stop or self.__stop < 1:
            raise StopIteration
        elif self.__step > 1:
            self.__seq = ''.join(
                [str(x.end() - x.start()) + x.string[x.start()] for x in self.__re.finditer(self.__seq)]
            )[:self.__length]

        self.__step += 1
        return self.__seq[:self.__length_ret]

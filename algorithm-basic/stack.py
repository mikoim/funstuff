class ListStack(object):
    def __init__(self, stackSize : int):
        self._stack = [None] * stackSize
        self._sp = -1

    def push(self, value):
        self._sp += 1
        self._stack[self._sp] = value
        return value

    def pop(self):
        self._sp -= 1
        return self._stack[self._sp + 1]

    def peek(self):
        return self._stack[self._sp]

    def isEmpty(self):
        return self._sp < 0


class LinkedListStack(object):
    pass

if __name__ == '__main__':
    ls = ListStack(10)

    print(
        ls.isEmpty(),
        ls.push(1),
        ls.peek(),
        ls.push(2),
        ls.peek(),
        ls.push(3),
        ls.peek(),
        ls.pop(),
        ls.pop(),
        ls.pop(),
        ls.isEmpty()
    )

class Cell(object):
    def __init__(self, item=None, next=None):
        self.item = item
        self.next = next

    def __eq__(self, other):
        if other == None:
            return False

        return self.item == other.item


def dump(linkedList: Cell):
    cell = linkedList

    while True:
        print(cell.item)

        if cell.next == None:
            break

        cell = cell.next


def insert_element_by_index(linkedList: Cell, index: int, element: Cell):
    if index == 0:
        return

    cell = linkedList

    for _ in range(1, index):
        cell = cell.next

    element.next = cell.next
    cell.next = element


def remove_element_last(linkedList: Cell):
    cur = linkedList
    prev = None

    while cur.next != None:
        prev = cur
        cur = cur.next

    prev.next = None


def remove_element_by_element(linkedList: Cell, element: Cell):
    cur = linkedList
    prev = None
    next = linkedList.next

    while True:
        if cur == element:
            prev.next = next
            break

        prev = cur
        cur = cur.next
        next = cur.next


if __name__ == '__main__':
    linkedList = Cell(1, Cell(2, Cell(3, Cell(4, None))))
    dump(linkedList)

    insert_element_by_index(linkedList, 2, Cell(100, None))
    dump(linkedList)

    remove_element_last(linkedList)
    dump(linkedList)

    remove_element_by_element(linkedList, Cell(2))
    dump(linkedList)

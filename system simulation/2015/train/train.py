class Train:
    def __init__(self, accelerator=2600, brake=-2700, distance=900):
        self.__accelerator = accelerator
        self.__brake = brake
        self.distance = distance
        self.__time = 0.0
        self.speed = 0.0
        self.position = 0.0
        self.history = []

    def reset(self):
        self.__time = 0.0
        self.speed = 0.0
        self.position = 0.0
        self.history = []

    def is_success(self, threshold=1) -> bool:
        if abs(self.distance - self.position) > threshold:
            return False
        elif self.speed > 0:
            return False
        else:
            return True

    def control(self, operations: list, debug=False) -> int:
        for operation in operations:
            if operation == 0:  # ' '
                pass
            elif operation == 1:  # 'a'
                self.speed += self.__accelerator
                if self.speed > 120000:
                    self.speed = 120000
            elif operation == 2:  # 'f'
                self.speed += (self.__accelerator / 2)
                if self.speed > 120000:
                    self.speed = 120000
            elif operation == -2:  # 'c'
                self.speed += (self.__brake / 2)
                if self.speed < 0:
                    self.speed = 0
            elif operation == -1:  # 'b'
                self.speed += self.__brake
                if self.speed < 0:
                    self.speed = 0

            self.position += self.speed / 3600
            self.__time += 1.0

            self.history.append((self.__time, self.position, self.speed))

            if debug:
                print(self.__time, self.position, self.speed)

            if self.is_success():
                if debug:
                    print("Success")

                break

        return self.__time

    @staticmethod
    def list2ascii(operations: list) -> str:
        result = ''

        for operation in operations:
            if operation == -2:
                result += 'c'
            elif operation == -1:
                result += 'b'
            elif operation == 0:
                result += ' '
            elif operation == 1:
                result += 'a'
            elif operation == 2:
                result += 'f'
            else:
                raise Exception('Unknown operator')

        return result

    @staticmethod
    def ascii2list(operations: str) -> list:
        result = []

        for operation in operations:
            if operation == 'c':
                result.append(-2)
            elif operation == 'b':
                result.append(-1)
            elif operation == ' ':
                result.append(0)
            elif operation == 'a':
                result.append(1)
            elif operation == 'f':
                result.append(2)
            else:
                raise Exception('Unknown operator')

        return result

if __name__ == '__main__':
    t = Train()
    data = input().split(',')
    t.distance = float(data[0])
    t.control(t.ascii2list(data[1]), debug=True)

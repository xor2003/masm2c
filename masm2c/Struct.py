
class Struct:
    def __init__(self, name):
        self.__name = name
        self.__data = list()
        self.__size = 0

    def append(self, data):
        self.__data.append(data)
        self.__size += data.getsize()

    def getdata(self):
        return self.__data

    def getsize(self):
        return self.__size



class Struct:
    def __init__(self, name):
        self.__name = name
        self.__data = list()

    def append(self, data):
        self.__data.append(data)

    def getdata(self):
        return self.__data


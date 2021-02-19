
class Macro:
    def __init__(self, name, parameters, repeat=1):
        self.__name = name
        self.__parameters = parameters
        self.instructions = []
        self.__repeat = repeat

    def getparameters(self):
        return self.__parameters

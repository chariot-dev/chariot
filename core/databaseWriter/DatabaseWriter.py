import abc


class DatabaseWriter(metaclass=abc.ABCMeta):
    """
        The purpose of this class is to act as an interface - it will have
        methods that all subclasses that write to databases must have
    """

    @abc.abstractmethod
    def writeToDB(self):
        pass

    @abc.abstractmethod
    def connectToDB(self):
        pass

    @abc.abstractmethod
    def disconnectFromDB(self):
        pass

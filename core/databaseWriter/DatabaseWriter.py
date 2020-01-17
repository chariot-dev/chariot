import abc


class DatabaseWriter(metaclass=abc.ABCMeta):
    """
        The purpose of this class is to act as an interface - it will have
        methods that all subclasses that write to databases must have
    """

    def __init__(self, db_path='database.db', flush=False):
        self.db_path = db_path
        self.flush = flush

    @abc.abstractmethod
    def initializeDB(self):
        pass

    @abc.abstractmethod
    def connectToDB(self):
        pass

    @abc.abstractmethod
    def disconnectFromDB(self):
        pass

    @abc.abstractmethod
    def insertRow(self, data):
        pass

    @abc.abstractmethod
    def flushDB(self):
        pass

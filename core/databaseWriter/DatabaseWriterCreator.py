import abc


class DatabaseWriterCreator(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def createDBWriter(self):
        """
            The purpose of this method is to return instances of Database writers that will interact
            with specific databases.
        """
        pass

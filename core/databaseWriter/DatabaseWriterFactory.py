import abc


class DatabaseWriterCreator(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def createDBWriter(self):
        """
            The purpose of this method is to return instances of Database writers that will interact
            with specific databases. The type is determined by the arguments passed to this method
        """
        pass

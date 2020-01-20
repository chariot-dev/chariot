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
        """
        Creates a new database instance.
        """
        pass

    @abc.abstractmethod
    def connectToDB(self):
        """
        Creates a new database if it does not exist, and generates a connection.

        Returns:
            A connection to the database.
        """
        pass

    @abc.abstractmethod
    def disconnectFromDB(self):
        """
        Deletes connection to the database.
        """
        pass

    @abc.abstractmethod
    def insertRow(self, relative_time, freeform):
        """
        Inserts a row into the database.

        Args:
            relative_time : Time since data collection initialized.
            freeform : JSON string containing device data.
        """
        pass

    @abc.abstractmethod
    def flushDB(self):
        """
        Removes all rows from the database.
        """
        pass


def main():
    pass


if __name__ == "__main__":
    main()

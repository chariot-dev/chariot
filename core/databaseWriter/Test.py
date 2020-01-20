from SqliteDBWriter import SqliteDBWriter
from MongoDBWriter import MongoDBWriter


def main():
    mongo = MongoDBWriter()
    mongo.insertRow(123, "hi")


if __name__ == "__main__":
    main()

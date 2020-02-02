from chariot.database.MongoDatabase import MongoDatabase

mongo = MongoDatabase()
mongo.insertRow(100, "hi")
print(__name__)

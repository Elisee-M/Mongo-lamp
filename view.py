from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["iot_db"]
collection = db["commands"]

print("All button presses:")
for doc in collection.find({}, {"_id": 0}):
    print(doc)
from pymongo import MongoClient

uri = "mongodb+srv://bridgetteliu821:bridgette123@cluster0.iprla7h.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["rocketchat"]
print(db.list_collection_names())
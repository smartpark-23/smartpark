from pymongo import MongoClient

# MongoDB Atlas Connection
MONGO_URL = "mongodb+srv://admin:admin123@cluster0.xnhfzb5.mongodb.net/SmartPark?retryWrites=true&w=majority"

client = MongoClient(MONGO_URL)

# Database
db = client["SmartPark"]

# Collections
users_collection = db["users"]
vehicles_collection = db["vehicles"]
parking_slots_collection = db["parking_slots"]
guest_collection = db["guest_parking"]
flats_collection = db["flats"]
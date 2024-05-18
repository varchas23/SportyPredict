from pymongo import MongoClient

# Replace with your MongoDB URI
mongo_uri = "mongodb+srv://SportyPredictAdmin:Password@sportypredict.fpxpjl1.mongodb.net/"
client = MongoClient(mongo_uri)

# Test the connection
print("Connected to MongoDB server successfully.")
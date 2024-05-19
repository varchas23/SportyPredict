# MongoDB Connect and Create Tables Database
#py install pymongo

from pymongo import MongoClient

# Connect to MongoDB Atlas (replace with your connection string)
client = MongoClient("mongodb+srv://SportyPredictAdmin:Password@sportypredict.fpxpjl1.mongodb.net/")

# Access your database
db = client.my_database

# Create a collection (table)
collection = db.PlayerStats

# Add record to see if works
mylist = [
    {"Name": "LeBron James", "Position": "SF", "PPG": 24.7, "APG": 6.2, "RPG": 7.4},
    {"Name": "Stephen Curry", "Position": "PG", "PPG": 27.2, "APG": 5.8, "RPG": 2.8}
    # Add more documents here
]
result = collection.insert_many(mylist)
print(result.inserted_ids)


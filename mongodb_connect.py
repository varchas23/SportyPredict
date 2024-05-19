# MongoDB Connect and Create Tables Database
#py install pymongo

from pymongo import MongoClient
from api_documentation import ApiNba

class MongoDB:
    def __init__(self):
        # Connect to MongoDB Atlas (replace with your connection string)
        self.client = MongoClient("mongodb+srv://SportyPredictAdmin:Password@sportypredict.fpxpjl1.mongodb.net/")

        # Access your database
        self.db = self.client.my_database

        # Create a collection (table)
        self.collection = self.db.PlayerStats

         # Create an instance of the ApiNba class
        api = ApiNba()

        # Fetch player data
        lebron_data = api.lebron()
        steph_data = api.steph()
        jokic_data = api.jokic()

        # Add record to see if it works
        self.players = [
            lebron_data,
            steph_data,
            jokic_data
        ]

        # Ensure each record is inserted correctly and print the result
        result = self.collection.insert_many(self.players)
        print(result.inserted_ids)

# Instantiate the MongoDB class to trigger the data insertion
mongo_db = MongoDB()

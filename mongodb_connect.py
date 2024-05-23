# MongoDB Connect and Create Tables Database

# Importing libraries
from pymongo import MongoClient, DESCENDING
from api_documentation import ApiNba

# Class to connect to MongoDB database and collects player data
class MongoDB:
    def __init__(self):
        # Connect to MongoDB Atlas
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

        # Add sample record
        self.players = [
            lebron_data,
            steph_data,
            jokic_data
        ]

        # Ensure each record is inserted correctly and print the result
        result = self.collection.insert_many(self.players)
    
        #print(result.inserted_ids)

    # Get game data for player in a list
    def games(self, playerName):
        records = self.collection.find({"response.player.firstname": playerName}).sort("response.game.id", DESCENDING)
        lst = list(records)
        return lst


# Instantiate the MongoDB class to trigger the data insertion
mongo_db = MongoDB()

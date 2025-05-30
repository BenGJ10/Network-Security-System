"""
This script extracts network data from a CSV file and pushes it to a MongoDB database.
It reads the CSV file, converts it to JSON format, and uploads it to a specified MongoDB collection.
"""

import os
import sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(f"Your MongoDB URL: {MONGO_DB_URL}")

import certifi 
import pandas as pd
import numpy as np
import pymongo
from pymongo.server_api import ServerApi
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop = True, inplace = True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_to_mongodb(self, records, database, collection):
        """
        Inserts a list of records into a specified MongoDB database and collection.

        Args:
            records (list): A list of dictionaries representing the documents to insert.
            database (str): The name of the target MongoDB database.
            collection (str): The name of the target collection within the database.

        Returns:
            int: The number of records successfully inserted into the collection. 
        """

        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL,  server_api = ServerApi('1'), tls = True, tlsCAFile = certifi.where()) # Creates a connection to a MongoDB server
            self.database = self.mongo_client[self.database] #  Selects a database from the MongoDB server

            self.collection = self.database[self.collection] # Selects a collection from the specified database
            self.collection.insert_many(self.records) # Inserts the records into the collection

            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
if __name__ == "__main__":
    FILE_PATH = "datasets/phishingData.csv"
    DATABASE = "BenGJ"
    collection = "NetworkData"
    network_obj = NetworkDataExtract()
    records = network_obj.csv_to_json_convertor(file_path = FILE_PATH)
    no_of_records = network_obj.insert_data_to_mongodb(records, DATABASE, collection)
    print(f"{no_of_records} records have been inserted successfully into the MongoDB Atlas.")
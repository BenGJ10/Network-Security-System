import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Replace <username> and <password> with your actual username and password
uri = "mongodb+srv://<username>:<password>@cluster0.sfppbhe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'), tls = True, tlsCAFile=certifi.where())

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You have successfully connected to MongoDB!")
except Exception as e:
    print(e)

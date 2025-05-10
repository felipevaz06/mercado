import datetime   # This will be needed later
import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']

# Connect to your MongoDB cluster:
client = MongoClient(MONGODB_URI)


# List all the databases in the cluster:
for db_info in client.list_database_names():
   print(db_info)


# Get a reference to the 'sample_mflix' database:
db = client['mercado']

# List all the collections in 'sample_mflix':
collections = db.list_collection_names()
for collection in collections:
   print(collection)

# from motor.motor_asyncio import AsyncIOMotorClient
# import os

# mongo_uri=os.getenv('MONGO_URI')

# # MONGO_URI = "mongodb+srv://legalassist_user:savera@cluster0.avqg25z.mongodb.net/?appName=Cluster0" 

# #
# client = AsyncIOMotorClient(mongo_uri)

# db = client["test"]

# conversation_collection = db["conversations"]

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import os

mongo_uri = os.getenv('MONGO_URI')

# Sync client — for LangGraph tools
sync_client = MongoClient(mongo_uri)
db = sync_client["test"]

# Async client — for FastAPI endpoints
async_client = AsyncIOMotorClient(mongo_uri)
async_db = async_client["test"]
conversation_collection = async_db["conversations"]

try:
    sync_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
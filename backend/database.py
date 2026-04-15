from motor.motor_asyncio import AsyncIOMotorClient
import os

mongo_uri=os.getenv('MONGO_URI')

# MONGO_URI = "mongodb+srv://legalassist_user:savera@cluster0.avqg25z.mongodb.net/?appName=Cluster0" 

#
client = AsyncIOMotorClient(mongo_uri)

db = client["test"]

conversation_collection = db["conversations"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
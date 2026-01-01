from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://legalassist_user:savera@cluster0.avqg25z.mongodb.net/?appName=Cluster0" # or Atlas URI
client = AsyncIOMotorClient(MONGO_URI)

db = client["legalassist"]
conversation_collection = db["conversations"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
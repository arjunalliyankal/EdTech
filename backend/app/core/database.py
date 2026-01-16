from motor.motor_asyncio import AsyncIOMotorClient
try:
    from mongomock_motor import AsyncMongoMockClient
except ImportError:
    AsyncMongoMockClient = None
from app.core.json_db import JsonClient
from app.core.config import settings

class Database:
    client = None

db = Database()

async def get_database():
    return db.client[settings.DATABASE_NAME]

async def connect_to_mongo():
    try:
        # Try connecting to real Mongo first
        db.client = AsyncIOMotorClient(settings.MONGODB_URL, serverSelectionTimeoutMS=2000)
        # Verify connection
        await db.client.server_info()
        print(f"Successfully connected to MongoDB at {settings.MONGODB_URL}")
    except Exception as e:
        print(f"Could not connect to real MongoDB ({e}). Falling back to Persistent JSON Mock.")
        db.client = JsonClient("db.json")
        print("Persistent JSON Database initialized (db.json). Your data will be saved!")

async def close_mongo_connection():
    db.client.close()
    print("Closed MongoDB connection")

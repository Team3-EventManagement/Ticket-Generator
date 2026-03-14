import os
from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_instance = Database()

async def init_db():
    mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    db_instance.client = AsyncIOMotorClient(mongo_url)
    db_instance.db = db_instance.client.ticket_db

async def close_db():
    if db_instance.client:
        db_instance.client.close()

def get_db():
    return db_instance.db

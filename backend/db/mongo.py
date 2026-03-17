"""
MongoDB here is only for:

User settings
Service connection status
API keys/tokens per service
"""
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

from dotenv import load_dotenv
import os
load_dotenv()


# Creating the clinet 
client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db     = client[os.getenv("MONGODB_DB_NAME")]


#collection name 
users_collection    = db["users"]
settings_collection = db["settings"]

#user operation
async def get_user(user_id:str) -> dict:
    user = await users_collection.find_one({"user_id": user_id})
    return user


async def create_user(user_id:str,name:str)-> dict:
    user_data={
        "user_id": user_id,
        "name": name,
        "created_at":__import__("datetime").datetime.utcnow()
    }
    await users_collection.insert_one(user_data)
    print(f"user is created with id {user_id}")
    return user_data

async def get_or_create_user(user_id: str, name: str = "User") -> dict:
    user = await get_user(user_id)
    if not user:
        user = await create_user(user_id, name)
    return user



# ── Settings operations ────────────────────────
async def save_settings(user_id: str, service: str, data: dict):
    await settings_collection.update_one(
        {"user_id": user_id, "service": service},
        {"$set": data},
        upsert=True
    )
    print(f"✅ Settings saved for {service}")

async def get_settings(user_id: str, service: str) -> dict:
    settings = await settings_collection.find_one(
        {"user_id": user_id, "service": service}
    )
    return settings or {}

async def get_all_settings(user_id: str) -> dict:
    cursor   = settings_collection.find({"user_id": user_id})
    settings = await cursor.to_list(length=100)
    return {s["service"]: s for s in settings}
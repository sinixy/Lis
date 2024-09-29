import motor.motor_asyncio

from config import DB_HOST, DB_NAME


client = motor.motor_asyncio.AsyncIOMotorClient(DB_HOST)
db = client[DB_NAME]
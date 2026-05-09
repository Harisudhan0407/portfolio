from pymongo import MongoClient
import os
from config import Config

def get_db():
    client = MongoClient(Config.MONGO_URI)
    # Try to get database from URI, fallback to 'portfolio_db'
    db = client.get_database() if client.get_database().name else client.portfolio_db
    return db

db = get_db()

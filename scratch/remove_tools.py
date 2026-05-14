from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv('MONGO_URI'))
db = client.get_default_database()
result = db.skills.delete_many({'category': 'Tools & Technologies'})
print(f'Deleted {result.deleted_count} skills with category "Tools & Technologies"')

import sys
import os

# Add the parent directory to the path so we can import database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db

def remove_unused_fields():
    print("Connecting to MongoDB and removing 'github', 'live_demo', and 'image' fields from projects...")
    
    # $unset removes the specified fields from the documents
    result = db.projects.update_many(
        {}, 
        {"$unset": {
            "github": "", 
            "live_demo": "", 
            "image": ""
        }}
    )
    
    print(f"Success! Updated {result.modified_count} projects in the database.")

if __name__ == "__main__":
    remove_unused_fields()

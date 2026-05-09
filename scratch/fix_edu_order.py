from database import db
from bson import ObjectId

def fix_edu_order():
    # Fetch all education
    edus = list(db.education.find())
    
    # Identify items
    be = None
    hslc = None
    sslc = None
    others = []
    
    for edu in edus:
        degree = edu.get('degree', '').upper()
        if 'B.E' in degree or 'COLLEGE' in degree:
            be = edu
        elif 'HSLC' in degree or 'HIGHER' in degree:
            hslc = edu
        elif 'SSLC' in degree or 'SECONDARY' in degree:
            sslc = edu
        else:
            others.append(edu)
            
    # Order for insertion (Oldest to Newest)
    # So that sort(-1) puts Newest (B.E) at top
    new_order = []
    if sslc: new_order.append(sslc)
    if hslc: new_order.append(hslc)
    if be: new_order.append(be)
    
    # Add others in their original relative order
    new_order.extend(others)
    
    if new_order:
        # Clear collection
        db.education.delete_many({})
        
        # Strip old IDs and re-insert
        for item in new_order:
            if '_id' in item: del item['_id']
            
        db.education.insert_many(new_order)
        print(f"Re-ordered {len(new_order)} education entries.")
    else:
        print("No education entries found to re-order.")

if __name__ == '__main__':
    fix_edu_order()

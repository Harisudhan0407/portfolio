from database import db

def migrate_education():
    profile = db.profile.find_one()
    if profile and 'education' in profile and db.education.count_documents({}) == 0:
        edu_list = profile['education']
        new_edu_list = []
        for edu in edu_list:
            new_edu_list.append({
                'degree': edu.get('degree', ''),
                'institution': edu.get('institution', ''),
                'date': edu.get('year', ''), # Seed uses 'year'
                'score': edu.get('score', '')
            })
        if new_edu_list:
            db.education.insert_many(new_edu_list)
            print(f"Migrated {len(new_edu_list)} education entries.")
    else:
        print("No migration needed or profile not found.")

if __name__ == '__main__':
    migrate_education()

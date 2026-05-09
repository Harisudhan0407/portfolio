from database import db

def reset_education():
    # Clear all education
    db.education.delete_many({})
    
    # Insert in order: SSLC (Oldest) -> HSLC -> B.E. (Newest)
    # So that sort('_id', -1) puts B.E. at the TOP
    new_edus = [
        {
            'degree': 'Secondary (SSLC)',
            'institution': 'SSV Matric Hr. Sec. School, Kuttapatti',
            'date': '2020 - 2021',
            'score': '78.4%'
        },
        {
            'degree': 'Higher Secondary (HSLC)',
            'institution': 'SSV Matric Hr. Sec. School, Kuttapatti',
            'date': '2021 - 2023',
            'score': '88%'
        },
        {
            'degree': 'B.E. Computer Science Engineering (IoT)',
            'institution': 'SNS Institutions, Coimbatore',
            'date': '2023 - Present',
            'score': '8.5 CGPA'
        }
    ]
    
    db.education.insert_many(new_edus)
    print("Education reset and re-ordered successfully.")

if __name__ == '__main__':
    reset_education()

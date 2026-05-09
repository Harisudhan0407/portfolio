from database import db
from datetime import datetime

def seed_db():
    # Profile
    if db.profile.count_documents({}) == 0:
        db.profile.insert_one({
            'name': 'HARISUDHAN K',
            'role': 'CSE (IoT) Student',
            'tagline': 'Building modern web experiences with creativity and technology.',
            'about': 'First-year engineering student specializing in Computer Science Engineering (IoT) with hands-on experience in Web Development, API Integration, and Flask.',
            'education': [
                {'institution': 'SNS Institutions, Coimbatore', 'degree': 'B.E. CSE (IoT)', 'year': '2023 - Present'},
                {'institution': 'Higher Secondary', 'degree': 'HSLC', 'score': '88%'},
                {'institution': 'Secondary', 'degree': 'SSLC', 'score': '78.4%'}
            ],
            'social': {
                'github': 'https://github.com/Harisudhan0407',
                'linkedin': 'https://www.linkedin.com/in/harisudhank/',
                'whatsapp': 'https://wa.me/919443286016',
                'email': 'mailto:harisudhan072008@gmail.com'
            }
        })
        print("Profile seeded.")

    # Skills
    if db.skills.count_documents({}) == 0:
        db.skills.insert_many([
            {'name': 'Flask', 'category': 'Backend', 'percent': 90},
            {'name': 'MongoDB', 'category': 'Database', 'percent': 80},
            {'name': 'HTML/CSS', 'category': 'Frontend', 'percent': 95},
            {'name': 'JavaScript', 'category': 'Frontend', 'percent': 85},
            {'name': 'n8n Automation', 'category': 'Tools', 'percent': 85}
        ])
        print("Skills seeded.")

    # Projects
    if db.projects.count_documents({}) == 0:
        db.projects.insert_one({
            'title': 'MedClinic AI',
            'description': 'AI-powered clinical support system helping users recover from health issues using AI suggestions.',
            'tags': ['Flask', 'MongoDB', 'AI'],
            'github': '#',
            'live_demo': '#',
            'image': None
        })
        print("Projects seeded.")

    # Education (New Collection)
    if db.education.count_documents({}) == 0:
        db.education.insert_many([
            {'institution': 'SNS Institutions, Coimbatore', 'degree': 'B.E. CSE (IoT)', 'date': '2023 - Present', 'score': '8.5 CGPA'},
            {'institution': 'SSV Matric Hr. Sec. School', 'degree': 'Higher Secondary (HSLC)', 'date': '2021 - 2023', 'score': '88%'},
            {'institution': 'SSV Matric Hr. Sec. School', 'degree': 'Secondary (SSLC)', 'date': '2020 - 2021', 'score': '78.4%'}
        ])
        print("Education seeded.")

if __name__ == '__main__':
    seed_db()

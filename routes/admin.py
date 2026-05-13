from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import db
from werkzeug.security import check_password_hash, generate_password_hash
import os
from config import Config
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
import cloudinary
import cloudinary.uploader

# Configure Cloudinary
cloudinary.config(
    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
    api_key=Config.CLOUDINARY_API_KEY,
    api_secret=Config.CLOUDINARY_API_SECRET
)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def is_logged_in():
    return 'admin_logged_in' in session

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        env_pass = os.getenv('ADMIN_PASSWORD', 'admin123')
        
        if password == env_pass:
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid password', 'danger')
            
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('main.index'))

@admin_bp.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect(url_for('admin.login'))
        
    stats = {
        'projects': db.projects.count_documents({}),
        'skills': db.skills.count_documents({}),
        'messages': db.contacts.count_documents({}),
        'certs': db.certifications.count_documents({}),
        'education': db.education.count_documents({})
    }
    projects = list(db.projects.find())
    skills = list(db.skills.find())
    certs = list(db.certifications.find())
    from datetime import datetime
    
    # Force fix order for main milestones
    education_raw = list(db.education.find())
    for edu in education_raw:
        deg = edu.get('degree', '').upper()
        ts = None
        if 'B.E' in deg or 'COLLEGE' in deg: ts = 3000000000 # Future date
        elif 'HSLC' in deg or 'HIGHER' in deg: ts = 2000000000
        elif 'SSLC' in deg or 'SECONDARY' in deg: ts = 1000000000
        
        if ts is not None:
            db.education.update_one({'_id': edu['_id']}, {'$set': {'timestamp': ts}})
            
    education = list(db.education.find().sort('timestamp', -1))
    
    # Initialization/Migration Logic
    if not education:
        # Default entries with explicit timestamps for correct order
        new_edu_list = [
            {'degree': 'Secondary (SSLC)', 'institution': 'SSV Matric Hr. Sec. School, Kuttapatti', 'date': '2020 - 2021', 'score': '78.4%', 'timestamp': 1},
            {'degree': 'Higher Secondary (HSLC)', 'institution': 'SSV Matric Hr. Sec. School, Kuttapatti', 'date': '2021 - 2023', 'score': '88%', 'timestamp': 2},
            {'degree': 'B.E. Computer Science Engineering (IoT)', 'institution': 'SNS Institutions, Coimbatore', 'date': '2023 - Present', 'score': '8.5 CGPA', 'timestamp': 3}
        ]
        db.education.insert_many(new_edu_list)
        education = list(db.education.find().sort('timestamp', -1))

    profile = db.profile.find_one()
    
    return render_template('admin/dashboard.html', 
                           stats=stats, 
                           projects=projects, 
                           skills=skills, 
                           certs=certs,
                           education=education,
                           profile=profile)

# Projects Management
@admin_bp.route('/projects')
def projects():
    if not is_logged_in(): return redirect(url_for('admin.login'))
    projects_list = list(db.projects.find())
    return render_template('admin/projects.html', projects=projects_list)

@admin_bp.route('/projects/add', methods=['POST'])
def add_project():
    if not is_logged_in(): return redirect(url_for('admin.login'))
    title = request.form.get('title')
    description = request.form.get('description')
    tags = request.form.get('tags').split(',')
    db.projects.insert_one({
        'title': title,
        'description': description,
        'tags': [t.strip() for t in tags]
    })
    flash('Project added successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/projects/update/<id>', methods=['POST'])
def update_project(id):
    if not is_logged_in(): return redirect(url_for('admin.login'))
    title = request.form.get('title')
    description = request.form.get('description')
    tags = request.form.get('tags').split(',')
    db.projects.update_one({'_id': ObjectId(id)}, {'$set': {
        'title': title,
        'description': description,
        'tags': [t.strip() for t in tags]
    }})
    flash('Project updated!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/projects/delete/<id>')
def delete_project(id):
    if not is_logged_in(): return redirect(url_for('admin.login'))
    db.projects.delete_one({'_id': ObjectId(id)})
    flash('Project deleted', 'info')
    return redirect(url_for('admin.dashboard'))

# Messages
@admin_bp.route('/messages')
def messages():
    if not is_logged_in(): return redirect(url_for('admin.login'))
    all_messages = list(db.contacts.find().sort('date', -1))
    return render_template('admin/messages.html', messages=all_messages)

# Profile Management
@admin_bp.route('/profile')
def profile():
    if not is_logged_in(): return redirect(url_for('admin.login'))
    profile_data = db.profile.find_one()
    return render_template('admin/profile.html', profile=profile_data)

@admin_bp.route('/profile/update', methods=['POST'])
def update_profile():
    if not is_logged_in(): return redirect(url_for('admin.login'))
    name = request.form.get('name')
    role = request.form.get('role')
    about_text = request.form.get('about')
    
    update_data = {}
    if name: update_data['name'] = name
    if role: update_data['role'] = role
    if about_text: update_data['about'] = about_text
    
    # Handle Photo Upload
    try:
        if request.form.get('cropped_image'):
            # Upload base64 cropped image to Cloudinary
            result = cloudinary.uploader.upload(request.form.get('cropped_image'), folder="portfolio/profile")
            update_data['image_url'] = result.get('secure_url')
        elif 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '':
                # Upload raw file directly to Cloudinary
                result = cloudinary.uploader.upload(file, folder="portfolio/profile")
                update_data['image_url'] = result.get('secure_url')
    except Exception as e:
        flash(f'Error uploading image: {str(e)}', 'error')
        return redirect(url_for('admin.dashboard'))
            
    db.profile.update_one({}, {'$set': update_data}, upsert=True)
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

# Skills Management
@admin_bp.route('/skills/add', methods=['POST'])
def add_skill():
    if not is_logged_in(): return redirect(url_for('admin.login'))
    name = request.form.get('name')
    category = request.form.get('category')
    proficiency = request.form.get('proficiency', 0)
    
    db.skills.insert_one({
        'name': name,
        'category': category,
        'proficiency': int(proficiency)
    })
    flash('Skill added!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/skills/delete/<id>')
def delete_skill(id):
    if not is_logged_in(): return redirect(url_for('admin.login'))
    db.skills.delete_one({'_id': ObjectId(id)})
    flash('Skill removed', 'info')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/skills/update/<id>', methods=['POST'])
def update_skill(id):
    if not is_logged_in(): return redirect(url_for('admin.login'))
    name = request.form.get('name')
    category = request.form.get('category')
    proficiency = request.form.get('proficiency', 0)
    
    db.skills.update_one({'_id': ObjectId(id)}, {'$set': {
        'name': name,
        'category': category,
        'proficiency': int(proficiency)
    }})
    flash('Skill updated!', 'success')
    return redirect(url_for('admin.dashboard'))

# Certifications Management
@admin_bp.route('/certs/add', methods=['POST'])
def add_cert():
    if not is_logged_in(): return redirect(url_for('admin.login'))
    name = request.form.get('name')
    issuer = request.form.get('issuer')
    date = request.form.get('date')
    
    cert_data = {
        'name': name,
        'issuer': issuer,
        'date': date
    }
    
    if 'cert_file' in request.files:
        file = request.files['cert_file']
        if file and file.filename != '':
            try:
                result = cloudinary.uploader.upload(file, folder="portfolio/certs")
                cert_data['file_url'] = result.get('secure_url')
            except Exception as e:
                flash(f'Error uploading certificate: {str(e)}', 'error')
                return redirect(url_for('admin.dashboard'))
            
    db.certifications.insert_one(cert_data)
    flash('Certification added!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/certs/update/<id>', methods=['POST'])
def update_cert(id):
    if not is_logged_in(): return redirect(url_for('admin.login'))
    name = request.form.get('name')
    issuer = request.form.get('issuer')
    date = request.form.get('date')
    
    update_data = {
        'name': name,
        'issuer': issuer,
        'date': date
    }
    
    if 'cert_file' in request.files:
        file = request.files['cert_file']
        if file and file.filename != '':
            try:
                result = cloudinary.uploader.upload(file, folder="portfolio/certs")
                update_data['file_url'] = result.get('secure_url')
            except Exception as e:
                flash(f'Error uploading certificate: {str(e)}', 'error')
                return redirect(url_for('admin.dashboard'))
            
    db.certifications.update_one({'_id': ObjectId(id)}, {'$set': update_data})
    flash('Certification updated!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/certs/delete/<id>')
def delete_cert(id):
    if not is_logged_in(): return redirect(url_for('admin.login'))
    db.certifications.delete_one({'_id': ObjectId(id)})
    flash('Certification removed', 'info')
    return redirect(url_for('admin.dashboard'))

# Education Management
@admin_bp.route('/education/add', methods=['POST'])
def add_education():
    if not is_logged_in(): return redirect(url_for('admin.login'))
    from datetime import datetime
    new_edu = {
        'degree': request.form.get('degree'),
        'institution': request.form.get('institution'),
        'date': request.form.get('date'),
        'score': request.form.get('score'),
        'timestamp': int(datetime.now().timestamp())
    }
    db.education.insert_one(new_edu)
    flash('Education added!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/education/update/<id>', methods=['POST'])
def update_education(id):
    if not is_logged_in(): return redirect(url_for('admin.login'))
    degree = request.form.get('degree')
    institution = request.form.get('institution')
    date = request.form.get('date')
    score = request.form.get('score')
    
    db.education.update_one({'_id': ObjectId(id)}, {'$set': {
        'degree': degree,
        'institution': institution,
        'date': date,
        'score': score
    }})
    flash('Education updated!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/education/delete/<id>')
def delete_education(id):
    if not is_logged_in(): return redirect(url_for('admin.login'))
    db.education.delete_one({'_id': ObjectId(id)})
    flash('Education removed', 'info')
    return redirect(url_for('admin.dashboard'))

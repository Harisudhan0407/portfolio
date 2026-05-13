from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import db
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    profile = db.profile.find_one()
    projects = list(db.projects.find().limit(3))
    skills = list(db.skills.find())
    return render_template('index.html', profile=profile, projects=projects, skills=skills)

@main_bp.route('/about')
def about():
    profile = db.profile.find_one()
    
    # Force fix order for main milestones
    education_raw = list(db.education.find())
    for edu in education_raw:
        deg = edu.get('degree', '').upper()
        ts = None
        if 'B.E' in deg or 'COLLEGE' in deg: ts = 3000000000
        elif 'HSLC' in deg or 'HIGHER' in deg: ts = 2000000000
        elif 'SSLC' in deg or 'SECONDARY' in deg: ts = 1000000000
        
        if ts is not None and edu.get('timestamp') != ts:
            db.education.update_one({'_id': edu['_id']}, {'$set': {'timestamp': ts}})
            
    education = list(db.education.find().sort('timestamp', -1))
    return render_template('about.html', profile=profile, education=education)

@main_bp.route('/skills')
def skills():
    skills_list = list(db.skills.find())
    return render_template('skills.html', skills=skills_list)

@main_bp.route('/projects')
def projects():
    projects_list = list(db.projects.find())
    return render_template('projects.html', projects=projects_list)

@main_bp.route('/certifications')
def certifications():
    certs = list(db.certifications.find())
    return render_template('certifications.html', certs=certs)

@main_bp.route('/experience')
def experience():
    internships = list(db.internships.find())
    hackathons = list(db.hackathons.find())
    return render_template('experience.html', internships=internships, hackathons=hackathons)

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        db.contacts.insert_one({
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'date': datetime.now()
        })
        flash('Message sent successfully!', 'success')
        return redirect(url_for('main.contact'))
        
    return render_template('contact.html')

@main_bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

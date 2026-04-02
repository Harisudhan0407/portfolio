import os
from flask import Flask, render_template, request, flash, redirect, url_for, session
from pymongo import MongoClient
from datetime import datetime
from functools import wraps
from bson.objectid import ObjectId
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_portfolio_secret")
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB max upload

# Photo upload config
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
PHOTO_UPLOAD_FOLDER = os.path.join(app.root_path, "static", "photos")
os.makedirs(PHOTO_UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_profile_photo_url():
    """Return the URL of the current profile photo from DB settings."""
    try:
        setting = db.settings.find_one({"_id": "profile_photo"})
        if setting and setting.get("filename"):
            return "/static/photos/" + setting["filename"]
    except Exception:
        pass
    return "/static/photos/Hari.jpeg"  # default fallback

# MongoDB Atlas connection
mongo_uri = os.getenv("MONGO_URI")

try:
    if mongo_uri:
        client = MongoClient(mongo_uri)
    else:
        client = MongoClient("mongodb://localhost:27017/")
    db = client["portfolio"]
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

# Admin authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function

# Seed default data if empty
def seed_default_data():
    try:
        if db.skills.count_documents({}) == 0:
            default_skills = [
                {"name": "Web Development", "percentage": 85, "category": "Technical"},
                {"name": "API Integration", "percentage": 80, "category": "Technical"},
                {"name": "MongoDB", "percentage": 75, "category": "Technical"},
                {"name": "n8n Workflow Automation", "percentage": 70, "category": "Technical"},
                {"name": "GitHub", "percentage": 85, "category": "Technical"},
                {"name": "Basic UI/UX Principles", "percentage": 75, "category": "Technical"},
                {"name": "Team Collaboration", "percentage": 95, "category": "Soft"},
                {"name": "Problem Solving", "percentage": 90, "category": "Soft"},
                {"name": "Continuous Learning", "percentage": 100, "category": "Soft"}
            ]
            db.skills.insert_many(default_skills)
            
        if db.about.count_documents({}) == 0:
            db.about.insert_one({
                "_id": "about_content",
                "intro": "I am a passionate technology enthusiast specializing in the intersection of Internet of Things (IoT) and modern web systems. With a strong interest in understanding how devices communicate and how intuitive user interfaces can control complex operations, I am driven to build solutions that are fast, robust, and meaningful. Team collaboration and problem-solving are at the core of my approach to learning and building.",
                "vision": "My goal as a first-year student is to continuously absorb new technological paradigms and frameworks while instantly applying them to real-world applications. By bridging the gap between hardware (IoT) and robust web architectures, I aim to lead and collaborate in teams building systems that actively improve everyday life and industrial processes.",
                "academic": [
                    {
                        "_id": str(ObjectId()),
                        "degree": "B.E. Computer Science Engineering (Internet of Things)",
                        "institution": "SNS Institutions, Coimbatore",
                        "period": "2025–2026",
                        "details": "Focusing on IoT protocols, embedded systems, and modern software engineering practices."
                    },
                    {
                        "_id": str(ObjectId()),
                        "degree": "Higher Secondary School Certificate (HSLC)",
                        "institution": "SSV Matric Hr. Sec. School, Kuttapatti",
                        "period": "",
                        "details": "Completed with an outstanding score of <strong>88%</strong>."
                    },
                    {
                        "_id": str(ObjectId()),
                        "degree": "Secondary School Leaving Certificate (SSLC)",
                        "institution": "SSV Matric Hr. Sec. School, Kuttapatti",
                        "period": "",
                        "details": "Completed with a strong score of <strong>78.4%</strong>."
                    }
                ]
            })
            
        if db.projects.count_documents({}) == 0:
            db.projects.insert_one({
                "title": "MedClinic AI – Clinical Support System",
                "icon": "fa-heartbeat",
                "github_url": "#",
                "live_url": "",
                "tags": "Web (HTML/CSS/JS), APIs, MongoDB, Python Backend",
                "description": "A robust web application that helps users recover from health issues using AI-based suggestions and clinical support mechanics.\n\nProblem Statement: There is a significant lack of accessible AI health guidance for individuals needing immediate, preliminary clinical support and advice during recovery.\n\nSolution: Developed an AI-based support system that intelligently interacts with users to suggest actionable health and recovery paths, acting as a supportive agent.\n\nFeatures:\n- Smart contextual suggestions\n- Intuitive user interaction flow\n- Secure data handling and storage"
            })
    except Exception as e:
        print("Warning: Could not connect to MongoDB. Ensure your local server is running or MONGO_URI is set.")

seed_default_data()

# PUBLIC ROUTES

@app.route("/")
def home():
    photo_url = get_profile_photo_url()
    return render_template("index.html", photo_url=photo_url)

@app.route("/about")
def about():
    try:
        about_data = db.about.find_one({"_id": "about_content"})
    except Exception:
        about_data = None
    return render_template("about.html", about=about_data)

@app.route("/projects")
def projects():
    try:
        projects_list = list(db.projects.find())
    except Exception:
        projects_list = []
    return render_template("projects.html", projects=projects_list)

@app.route("/skills")
def skills():
    try:
        skills_list = list(db.skills.find())
        technical_skills = [s for s in skills_list if s.get("category") == "Technical"]
        soft_skills = [s for s in skills_list if s.get("category") == "Soft"]
    except Exception:
        flash("Could not connect to database. Showing empty skills.", "error")
        technical_skills, soft_skills = [], []
    return render_template("skills.html", technical_skills=technical_skills, soft_skills=soft_skills)

@app.route("/certificates")
def certificates():
    try:
        certs = list(db.certificates.find())
    except Exception:
        flash("Could not connect to database. Showing empty certificates.", "error")
        certs = []
    return render_template("certificates.html", certificates=certs)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        try:
            db.messages.insert_one({
                "name": request.form.get("name"),
                "email": request.form.get("email"),
                "message": request.form.get("message"),
                "date": datetime.utcnow()
            })
            flash("Message sent successfully!", "success")
            return redirect(url_for("contact"))
        except Exception as e:
            flash(f"An error occurred: {e}", "error")
    return render_template("contact.html")

# ADMIN ROUTES

@app.route("/admin")
def admin_home():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))
    return redirect(url_for("admin_login"))

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password")
        admin_pass = os.getenv("ADMIN_PASSWORD", "admin123")
        
        # Check if password matches (handling both plain text and hash)
        is_valid = False
        if password == admin_pass:
            is_valid = True
        elif check_password_hash(admin_pass, password):
            is_valid = True
            
        if is_valid:
            session["admin_logged_in"] = True
            flash("Logged in successfully.", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid password.", "error")
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    flash("Logged out.", "success")
    return redirect(url_for("home"))

@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    try:
        about_data = db.about.find_one({"_id": "about_content"})
        skills_list = list(db.skills.find())
        certs_list = list(db.certificates.find())
        projects_list = list(db.projects.find())
        messages_list = list(db.messages.find().sort("date", -1))
        
        counts = {
            "skills": len(skills_list),
            "certificates": len(certs_list),
            "projects": len(projects_list),
            "messages": len(messages_list)
        }
    except Exception:
        flash("Database connection error. Dashboard features will fail.", "error")
        about_data = None
        skills_list, certs_list, projects_list, messages_list, counts = [], [], [], [], {}
    photo_url = get_profile_photo_url()
    return render_template("admin_dashboard.html", 
        about=about_data, skills=skills_list, certificates=certs_list, 
        projects=projects_list, messages=messages_list, counts=counts,
        photo_url=photo_url)

@app.route("/admin/upload_photo", methods=["POST"])
@login_required
def admin_upload_photo():
    if "photo" not in request.files:
        flash("No file selected.", "error")
        return redirect(url_for("admin_dashboard"))
    
    file = request.files["photo"]
    if file.filename == "":
        flash("No file selected.", "error")
        return redirect(url_for("admin_dashboard"))
    
    if file and allowed_file(file.filename):
        try:
            ext = file.filename.rsplit(".", 1)[1].lower()
            # Use a timestamp to bust browser cache
            import time
            filename = "profile_" + str(int(time.time())) + "." + ext
            filepath = os.path.join(PHOTO_UPLOAD_FOLDER, filename)
            file.save(filepath)
            # Delete old profile photos to keep folder clean
            for f in os.listdir(PHOTO_UPLOAD_FOLDER):
                if f.startswith("profile_") and f != filename:
                    try:
                        os.remove(os.path.join(PHOTO_UPLOAD_FOLDER, f))
                    except Exception:
                        pass
            # Store in DB
            db.settings.update_one(
                {"_id": "profile_photo"},
                {"$set": {"filename": filename}},
                upsert=True
            )
            flash("Profile photo updated successfully!", "success")
        except Exception as e:
            flash(f"Upload failed: {str(e)}", "error")
    else:
        flash("Invalid file type. Allowed: png, jpg, jpeg, gif, webp.", "error")
    
    return redirect(url_for("admin_dashboard") + "#photo-tab")

@app.route("/admin/about/update_text", methods=["POST"])
@login_required
def admin_update_about_text():
    db.about.update_one(
        {"_id": "about_content"},
        {"$set": {
            "intro": request.form.get("intro"),
            "vision": request.form.get("vision")
        }},
        upsert=True
    )
    flash("About text updated successfully.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/about/academic/add", methods=["POST"])
@login_required
def admin_add_academic():
    db.about.update_one(
        {"_id": "about_content"},
        {"$push": {
            "academic": {
                "_id": str(ObjectId()),
                "degree": request.form.get("degree"),
                "institution": request.form.get("institution"),
                "period": request.form.get("period", ""),
                "details": request.form.get("details", "")
            }
        }}
    )
    flash("Academic entry added.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/about/academic/delete/<acad_id>", methods=["POST"])
@login_required
def admin_delete_academic(acad_id):
    db.about.update_one(
        {"_id": "about_content"},
        {"$pull": {
            "academic": {"_id": acad_id}
        }}
    )
    flash("Academic entry deleted.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/about/academic/edit/<acad_id>", methods=["POST"])
@login_required
def admin_edit_academic(acad_id):
    db.about.update_one(
        {"_id": "about_content", "academic._id": acad_id},
        {"$set": {
            "academic.$.degree": request.form.get("degree"),
            "academic.$.institution": request.form.get("institution"),
            "academic.$.period": request.form.get("period", ""),
            "academic.$.details": request.form.get("details", "")
        }}
    )
    flash("Academic entry updated.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/skill/add", methods=["POST"])
@login_required
def admin_add_skill():
    db.skills.insert_one({
        "name": request.form.get("name"),
        "percentage": int(request.form.get("percentage", 0)),
        "category": request.form.get("category")
    })
    flash("Skill added successfully.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/skill/delete/<skill_id>", methods=["POST"])
@login_required
def admin_delete_skill(skill_id):
    db.skills.delete_one({"_id": ObjectId(skill_id)})
    flash("Skill deleted successfully.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/skill/edit/<skill_id>", methods=["POST"])
@login_required
def admin_edit_skill(skill_id):
    db.skills.update_one(
        {"_id": ObjectId(skill_id)},
        {"$set": {
            "name": request.form.get("name"),
            "percentage": int(request.form.get("percentage", 0)),
            "category": request.form.get("category")
        }}
    )
    flash("Skill updated successfully.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/certificate/add", methods=["POST"])
@login_required
def admin_add_certificate():
    db.certificates.insert_one({
        "title": request.form.get("title"),
        "issuer": request.form.get("issuer"),
        "date": request.form.get("date"),
        "link": request.form.get("link"),
        "description": request.form.get("description")
    })
    flash("Certificate added successfully.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/certificate/delete/<cert_id>", methods=["POST"])
@login_required
def admin_delete_certificate(cert_id):
    db.certificates.delete_one({"_id": ObjectId(cert_id)})
    flash("Certificate deleted successfully.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/certificate/edit/<cert_id>", methods=["POST"])
@login_required
def admin_edit_certificate(cert_id):
    db.certificates.update_one(
        {"_id": ObjectId(cert_id)},
        {"$set": {
            "title": request.form.get("title"),
            "issuer": request.form.get("issuer"),
            "date": request.form.get("date"),
            "link": request.form.get("link"),
            "description": request.form.get("description")
        }}
    )
    flash("Certificate updated successfully.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/project/add", methods=["POST"])
@login_required
def admin_add_project():
    db.projects.insert_one({
        "title": request.form.get("title"),
        "icon": request.form.get("icon"),
        "github_url": request.form.get("github_url"),
        "live_url": request.form.get("live_url"),
        "tags": request.form.get("tags"),
        "description": request.form.get("description")
    })
    flash("Project added successfully.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/project/delete/<project_id>", methods=["POST"])
@login_required
def admin_delete_project(project_id):
    db.projects.delete_one({"_id": ObjectId(project_id)})
    flash("Project deleted successfully.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/project/edit/<project_id>", methods=["POST"])
@login_required
def admin_edit_project(project_id):
    db.projects.update_one(
        {"_id": ObjectId(project_id)},
        {"$set": {
            "title": request.form.get("title"),
            "icon": request.form.get("icon"),
            "github_url": request.form.get("github_url"),
            "live_url": request.form.get("live_url"),
            "tags": request.form.get("tags"),
            "description": request.form.get("description")
        }}
    )
    flash("Project updated successfully.", "success")
    return redirect(url_for("admin_dashboard"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)

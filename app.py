from flask import Flask, render_template, request
from config import Config
from routes.main import main_bp
from routes.admin import admin_bp
import os

app = Flask(__name__)
app.config.from_object(Config)

# Secure session cookies
app.config['SESSION_COOKIE_HTTPONLY'] = True   # JS cannot read the cookie
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' # CSRF protection
app.config['SESSION_COOKIE_SECURE'] = False    # Set True only when using HTTPS in production

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Register Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(admin_bp)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Security Headers — protect against XSS, clickjacking, MIME sniffing
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

if __name__ == '__main__':
    app.run(debug=True)


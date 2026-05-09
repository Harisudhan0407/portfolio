from flask import Flask, render_template
from config import Config
from routes.main import main_bp
from routes.admin import admin_bp
import os

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Register Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(admin_bp)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)

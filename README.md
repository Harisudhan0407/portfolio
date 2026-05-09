# Futuristic Luxury Portfolio - HARISUDHAN K

A premium, modern, and futuristic full-stack developer portfolio built with Python Flask and MongoDB.

## Features
- **Futuristic Design**: Glassmorphism, neon gradients, and royal typography.
- **Dynamic Content**: Projects, skills, and certifications managed via an Admin Dashboard.
- **3D Interactions**: Card tilt effects, custom cursor, and smooth scroll animations.
- **Full Stack**: Flask backend with MongoDB Atlas integration.
- **Secure Admin**: Protected dashboard for managing portfolio content and viewing messages.

## Tech Stack
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (Vanilla)
- **Backend**: Python Flask
- **Database**: MongoDB
- **Animations**: Particles.js, CSS Keyframes

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- MongoDB installed locally or a MongoDB Atlas URI.

### 2. Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Harisudhan0407/portfolio.git
   cd portfolio
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration
Create a `.env` file in the root directory (template provided in `.env.example` or use the one generated):
```env
SECRET_KEY=your_secret_key
MONGO_URI=mongodb://localhost:27017/portfolio_db
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

### 4. Database Seeding
Run the seed script to populate initial data:
```bash
python seed_db.py
```

### 5. Run the Application
```bash
python app.py
```
Visit `http://127.0.0.1:5000` to view your portfolio.

## Deployment Guide (Vercel)
1. Push your code to GitHub.
2. Connect your repository to Vercel.
3. Add Environment Variables (`MONGO_URI`, `SECRET_KEY`, etc.) in Vercel settings.
4. Ensure `vercel.json` is configured (if needed) or let Vercel auto-detect the Flask app.

## License
MIT License

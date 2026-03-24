# Harisudhan K - Professional Portfolio

This is a modern, responsive, and professional full-stack portfolio website built for Harisudhan K. It features a deep navy and gold aesthetic, glassmorphism cards, parallax scrolling, 3D floating shapes, and animated skill bars.

## Features
- **Frontend**: Vanilla HTML/CSS/JavaScript with responsive layout.
- **Backend**: Python Flask handling routing and contact form submissions.
- **Database**: MongoDB Atlas integration for storing contact messages.
- **Design Elements**:
  - Consistent deep navy & gold color scheme.
  - Interactive parallax background and floating 3D elements.
  - Scroll-triggered animations and skill bars.

## Pages
1. **Home** (`/`): Brief introduction and academic highlights.
2. **About** (`/about`): Detailed academic background and career vision in IoT/Web systems.
3. **Projects** (`/projects`): Showcases the MedClinic AI clinical support system.
4. **Skills** (`/skills`): Animated breakdown of technical API/Web/IoT skills and soft skills.
5. **Contact** (`/contact`): Contact details and a working contact form writing directly to MongoDB.

## Requirements
- Python 3.8+
- MongoDB Atlas account (or local MongoDB database)

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Set the following environment variables (or create a `.env` file if using `python-dotenv`):
   ```bash
   # MongoDB Atlas Connection URI
   MONGO_URI="mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority"
   
   # Flask Session Secret Key
   SECRET_KEY="your-secret-key"
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Access the Application**
   Open your web browser and navigate to:
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Design Notes
- No UI changes or alterations from the core theme requests were made; the design strictly adhered to the classic + royal + professional guidelines requested.
- Content specifically reflects Harisudhan K's educational background and project summaries with no filler text.

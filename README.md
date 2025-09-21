# GlobalHire (Modern Starter)

This is a modern, animated Flask starter website for accepting job applications and sending them to your Gmail.

## Features
- Home page with futuristic animations, fake testimonials, and fake member stats
- Apply form with extended fields + resume upload (PDF/DOC/DOCX)
- Contact page
- Success page
- Styled with modern glassmorphism + CSS animations

## Setup (Local)
1. Install Python 3.10+ and pip.
2. Create virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate   # Windows
   ```
3. Install requirements:
   ```
   pip install -r requirements.txt
   ```
4. Configure Gmail environment variables (recommended):
   - `MAIL_USERNAME` = your Gmail address
   - `MAIL_PASSWORD` = your Gmail **App Password** (generate via Google Account -> Security -> App passwords)
   - Optionally: `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `FLASK_SECRET`
5. Run:
   ```
   python app.py
   ```
6. Open http://localhost:5000

## Deploy to Render
1. Push repo to GitHub.
2. Create a new Web Service on Render and connect your repo.
3. Set environment variables on Render (MAIL_USERNAME, MAIL_PASSWORD, FLASK_SECRET).
4. Use build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. Deploy.

## Important: Gmail
- Google requires 2-Step Verification enabled and an App Password for SMTP access.
- Do not commit real passwords to the repository. Use environment variables.


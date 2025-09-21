from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_mail import Mail, Message
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "change-me-please")

# Mail config (use env vars in production)
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'YOUR_GMAIL@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'YOUR_APP_PASSWORD')

# Upload config
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

mail = Mail(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    # fake stats for homepage
    stats = {
        "members": 2847,
        "jobs_posted": 192,
        "places": 27
    }
    testimonials = [
        {"name":"Aisha K.","role":"Caregiver","text":"GlobalHire helped me find work abroad in just 2 weeks! Highly recommend."},
        {"name":"Mohammed R.","role":"Driver","text":"Professional and fast — they guided me through every step."},
        {"name":"Lina S.","role":"Nurse","text":"Great support, trusted employers. I am now working overseas."}
    ]
    return render_template("index.html", stats=stats, testimonials=testimonials)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/apply", methods=["GET", "POST"])
def apply():
    if request.method == "POST":
        # collect form fields
        first_name = request.form.get("first_name","").strip()
        last_name = request.form.get("last_name","").strip()
        dob = request.form.get("dob","").strip()
        phone = request.form.get("phone","").strip()
        email = request.form.get("email","").strip()
        country = request.form.get("country","").strip()
        education = request.form.get("education","").strip()
        experience = request.form.get("experience","").strip()
        preferred = request.form.get("preferred","").strip()
        job_type = request.form.get("job_type","").strip()
        message = request.form.get("message","").strip()

        # handle file upload
        resume_filename = None
        if 'resume' in request.files:
            file = request.files['resume']
            if file and file.filename != '':
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(resume_path)
                    resume_filename = resume_path
                else:
                    flash("Resume must be PDF or DOC/DOCX.", "warning")
                    return redirect(url_for('apply'))

        # compose email body
        body = f"""New Job Application

Name: {first_name} {last_name}
Date of Birth: {dob}
Phone: {phone}
Email: {email}
Country: {country}
Education: {education}
Years Experience: {experience}
Preferred Job Type: {job_type}
What job would you want: {preferred}

Message:
{message}
"""

        try:
            msg = Message(subject=f"GlobalHire Application — {first_name} {last_name}",
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[app.config['MAIL_USERNAME']],
                          body=body)
            # attach resume if exists
            if resume_filename:
                with open(resume_filename, 'rb') as fp:
                    fname = os.path.basename(resume_filename)
                    msg.attach(fname, "application/octet-stream", fp.read())
            mail.send(msg)
        except Exception as e:
            app.logger.exception("Mail send failed:")
            flash("Application submitted but failed to send email. Please contact us if you don't receive confirmation.", "warning")
            return render_template("success.html", name=first_name)

        flash("Application sent successfully!", "success")
        return render_template("success.html", name=first_name)

    return render_template("apply.html")

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

"""This script launches the Flask server and renders the portfolio page."""
from flask import Flask, render_template, request
from flask_recaptcha import ReCaptcha  # Import ReCaptcha object
from flask_compress import Compress
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import smtplib
import datetime as dt

OWN_EMAIL = os.getenv('mail')
OWN_PASSWORD = os.getenv('pass')


app = Flask(__name__)
compress = Compress()
compress.init_app(app)
app.config['RECAPTCHA_SITE_KEY'] = \
    os.getenv('key_site')  # <-- Add your site key
app.config['RECAPTCHA_SECRET_KEY'] = \
    os.getenv('key_secret')  # <-- Add your secret key
recaptcha = ReCaptcha(app)  # Create a ReCaptcha object


@app.route("/")
def home():
    """Render index.html template."""
    current_year = dt.datetime.now().year
    return render_template('index.html', year=current_year)


@app.route("/submit", methods=["POST"])
def receive_data():
    """Receive the input from the contact section."""
    if request.method == "POST":
        if recaptcha.verify():
            name = request.form["name"]
            mail = request.form["mail"]
            message = request.form["message"]
            send_email(name, mail, message)
            return render_template('submission.html')
        else:
            return render_template('index.html')


def send_email(name, email, message):
    """Send email using Gmail SMTP."""
    email_message = \
        f"Name: {name}\nEmail: {email}\nMessage:{message}"
    msg = MIMEMultipart()
    msg['From'] = OWN_EMAIL
    msg['To'] = OWN_EMAIL
    msg['Subject'] = 'Contact Portfolio'
    msg.attach(MIMEText(email_message, "plain"))
    text = msg.as_string()
    
    # Using Gmail SMTP
    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.ehlo()
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, text)


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['RECAPTCHA_SIZE'] = 'compact'
    app.run(port=5000, host='0.0.0.0', debug=True)

from flask import Flask, render_template, request
from flask_recaptcha import ReCaptcha # Import ReCaptcha object
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import random
import smtplib
import datetime as dt
load_dotenv(os.path.join(os.path.dirname(__file__), 'keys.env'))

OWN_EMAIL = os.getenv('mail')
OWN_PASSWORD = os.getenv('pass')

app = Flask(__name__)
app.config['RECAPTCHA_SITE_KEY'] = os.getenv('key_site') # <-- Add your site key
app.config['RECAPTCHA_SECRET_KEY'] = os.getenv('key_secret') # <-- Add your secret key
recaptcha = ReCaptcha(app) # Create a ReCaptcha object by passing in 'app' as parameter

@app.route("/")
def hello_world():
    current_year = dt.datetime.now().year
    return render_template('index.html', year = current_year)

@app.route("/submit", methods=["POST"])
def receive_data():
    if request.method == "POST":
        if recaptcha.verify():
            name = request.form["name"]
            mail = request.form["mail"]
            phone = request.form["phone"]
            message = request.form["message"]
            send_email(name, mail, phone, message)
            return render_template('submission.html')
        else:
            return render_template('index.html')

def send_email(name, email, phone, message):
    email_message = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    msg = MIMEMultipart()
    msg['To']= OWN_EMAIL  
    msg['Subject']='Contact Portfolio'
    msg.attach(MIMEText(email_message, "plain"))
    text = msg.as_string()
    with smtplib.SMTP(host='smtp-mail.outlook.com', port=587) as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, text)

if __name__=='__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['RECAPTCHA_SIZE'] = 'compact'
    # port = 5000 + random.randint(0, 999)
    # url = f"http://127.0.0.1:{port}"
    app.run(debug=True, port=5000, host="0.0.0.0")
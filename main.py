from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import random
import smtplib
import datetime as dt
load_dotenv(os.path.join(os.path.dirname(__file__), 'keys.env'))

OWN_EMAIL = os.getenv('mail')
OWN_PASSWORD = os.getenv('pass')

app = Flask(__name__)

@app.route("/")
def hello_world():
    current_year = dt.datetime.now().year
    return render_template('index.html', year = current_year)

@app.route("/submit", methods=["POST"])
def receive_data():
    if request.method == "POST":
        name = request.form["name"]
        mail = request.form["mail"]
        phone = request.form["phone"]
        message = request.form["message"]
        send_email(name, mail, phone, message)
        return render_template('submission.html')

def send_email(name, email, phone, message):
    email_message = f"Subject:Contact Portfolio\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    print(email_message)
    with smtplib.SMTP(host='smtp-mail.outlook.com', port=587) as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message.encode('utf-8'))

if __name__=='__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    # port = 5000 + random.randint(0, 999)
    # url = f"http://127.0.0.1:{port}"
    app.run(debug=True, port=5000, host="0.0.0.0")
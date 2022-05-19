from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

if __name__=='__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    port = 5000 + random.randint(0, 999)
    url = f"http://127.0.0.1:{port}"
    app.run(debug=True, port=port)
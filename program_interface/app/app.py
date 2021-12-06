from flask import Flask, render_template

app = Flask(__name__)
application = app

@app.route('/')
def index():
    return render_template('index.html')

from lab01 import bp as lab01_bp
app.register_blueprint(lab01_bp)

from lab02 import bp as lab02_bp
app.register_blueprint(lab02_bp)

from lab03 import bp as lab03_bp
app.register_blueprint(lab03_bp)
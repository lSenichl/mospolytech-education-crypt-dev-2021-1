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

from lab04 import bp as lab04_bp
app.register_blueprint(lab04_bp)

from lab05 import bp as lab05_bp
app.register_blueprint(lab05_bp)

from lab06 import bp as lab06_bp
app.register_blueprint(lab06_bp)

from lab07 import bp as lab07_bp
app.register_blueprint(lab07_bp)

from lab08 import bp as lab08_bp
app.register_blueprint(lab08_bp)

from lab09 import bp as lab09_bp
app.register_blueprint(lab09_bp)

from lab10 import bp as lab10_bp
app.register_blueprint(lab10_bp)

from lab11 import bp as lab11_bp
app.register_blueprint(lab11_bp)
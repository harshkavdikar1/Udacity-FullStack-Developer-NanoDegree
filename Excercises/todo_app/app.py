from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Create an application with same name as name of the module
app = Flask(__name__)

@app.route("/")
def index():
    # Flask will look for this file in templates folder
    render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)